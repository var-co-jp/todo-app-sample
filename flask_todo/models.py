from flask_todo import db, login_manager
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import UserMixin

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
    due = db.Column(db.DateTime, nullable=False)
    detail = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    