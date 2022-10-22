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
    
    
    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = generate_password_hash(password)
        
    def validate_password(self, password):
        return check_password_hash(self.password, password)
    
    def add_user_db(self):
        try:
            with db.session.begin(subtransactions=True):
                db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()
            
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

    def __init__(self, title, due, detail):
        self.title = title
        self.due = due
        self.detail = detail
    
    def add_task_db(self):
        try:
            with db.session.begin(subtransactions=True):
                db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()
            
    def edit_task_db(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()
            
    def delete_task_db(self):
        try:
            with db.session.begin(subtransactions=True):
                db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()