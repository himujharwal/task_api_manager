
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)

    tasks_list = relationship("Task", back_populates="user")

    

    def set_password(self, password):
        self.password  = generate_password_hash(password)
        
        
    def check_password(self, password):
        return check_password_hash(self.password,password)
       


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="tasks_list")
