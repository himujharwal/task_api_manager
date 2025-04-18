
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))

    tasks_list = relationship("Task", back_populates="user")


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70))
    user_id = db.Column(db.Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="tasks_list")
