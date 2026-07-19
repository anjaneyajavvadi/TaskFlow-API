from flask import Blueprint,request,jsonify
from flask_jwt_extended import jwt_required,get_jwt_identity

from app.extensions import db
from app.models.task import Task
from app.schemas import TaskSchema

task_bp=Blueprint("tasks",__name__)

task_schema=TaskSchema()
tasks_schema=TaskSchema(many=True)

@task_bp.post("/")
@jwt_required()
def create_task():
    data=task_schema.load(request.json)

    task = Task(
        title=data["title"],
        description=data.get("description"),
        status=data.get("status", "pending"),
        priority=data.get("priority", "medium"),
        due_date=data.get("due_date"),
        user_id=int(get_jwt_identity())
    )

    db.session.add(task)
    db.session.commit()

    return jsonify({
        "message": "Task created successfully",
        "task": task_schema.dump(task)
    }), 201

@task_bp.get("/")
@jwt_required()
def get_tasks():
    query=Task.query.filter_by(user_id=int(get_jwt_identity()))

    status=request.args.get("status")
    priority=request.args.get("priority")
    title=request.args.get("title")

    if status:
        query=query.filter(Task.status==status)
    
    if priority:
        query = query.filter(Task.priority == priority)

    if title:
        query = query.filter(Task.title.ilike(f"%{title}%"))

    tasks = query.order_by(Task.created_at.desc()).all()

    return jsonify({
        "count": len(tasks),
        "tasks": tasks_schema.dump(tasks)
    }), 200

@task_bp.get("/<int:task_id>")
@jwt_required()
def get_task(task_id):

    task = Task.query.filter_by(
        id=task_id,
        user_id=int(get_jwt_identity())
    ).first()

    if not task:
        return jsonify({
            "message": "Task not found"
        }), 404

    return jsonify(task_schema.dump(task)), 200


@task_bp.put("/<int:task_id>")
@jwt_required()
def update_task(task_id):

    task = Task.query.filter_by(
        id=task_id,
        user_id=int(get_jwt_identity())
    ).first()

    if not task:
        return jsonify({
            "message": "Task not found"
        }), 404

    data = task_schema.load(request.json, partial=True)

    for key, value in data.items():
        setattr(task, key, value)

    db.session.commit()

    return jsonify({
        "message": "Task updated successfully",
        "task": task_schema.dump(task)
    }), 200

@task_bp.delete("/<int:task_id>")
@jwt_required()
def delete_task(task_id):

    task = Task.query.filter_by(
        id=task_id,
        user_id=int(get_jwt_identity())
    ).first()

    if not task:
        return jsonify({
            "message": "Task not found"
        }), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({
        "message": "Task deleted successfully"
    }), 200