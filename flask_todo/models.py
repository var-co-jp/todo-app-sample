from flask_todo import db, login_manager
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.sql import func

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(UserMixin, db.Model):
    # テーブル名
    __tablename__ = 'users'
    
    # カラム定義
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), index=True)
    password = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    update_at = db.Column(db.DateTime, nullable=True)
    last_access = db.Column(db.DateTime, onupdate=func.now(), nullable=True)
    
    
    tasks = db.relationship("Task", backref="users")
    
    
    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = generate_password_hash(password)
        
    def validate_password(self, password):
        return check_password_hash(self.password, password)
            
    @classmethod
    def select_by_email(cls, email):
        return cls.query.filter_by(email=email).first()


class Task(db.Model):
    # テーブル名
    __tablename__ = 'tasks'

    # カラム定義
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(64), index=True, nullable=False)
    detail = db.Column(db.String(128), index=True)
    end_time = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    update_at = db.Column(db.DateTime, onupdate=func.utc_timestamp(), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    