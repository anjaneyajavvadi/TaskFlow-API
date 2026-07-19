from flask import Blueprint,request,jsonify
from flask_jwt_extended import create_access_token

from app.extensions import db
from app.models.user import User
from app.schemas import RegisterSchema,LoginSchema,UserSchema

auth_bp=Blueprint("auth",__name__)

register_schema=RegisterSchema()
login_schema=LoginSchema()
user_schema=UserSchema()

@auth_bp.post("/register")
def register():
    data=register_schema.load(request.json)

    if(User.query.filter_by(email=data['email']).first()):
        return jsonify({"message":"Email already Exists"}),400
    
    user=User(
        username=data['username'],
        email=data['email']
    )

    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message":"User registered successfully",
        "user":user_schema.dump(user)
    }),201

@auth_bp.post("/login")
def login():
    data = login_schema.load(request.json)

    user = User.query.filter_by(email=data["email"]).first()

    if not user or not user.check_password(data["password"]):
        return jsonify({"message": "Invalid email or password"}), 401

    token = create_access_token(identity=str(user.id))

    return jsonify({
        "access_token": token,
        "user": user_schema.dump(user)
    }), 200

    