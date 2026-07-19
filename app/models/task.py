from datetime import datetime
from app.extensions import db

class Task(db.Model):
    __tablename__="tasks"

    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(150),nullable=False)
    description=db.Column(db.Text)
    status=db.Column(db.String(20),default="pending")
    priority=db.Column(db.String(20),default="medium")
    due_date=db.Column(db.Date)
    created_at=db.Column(db.DateTime,default=datetime.utcnow)
    updated_at=db.Column(
    db.DateTime,
    default=datetime.utcnow,
    onupdate=datetime.utcnow
    )

    user_id=db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    user=db.relationship(
        "User",
        back_populates="tasks"
    )
