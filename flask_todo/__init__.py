from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = 'todo_app.login'
login_manager.login_message = 'ログインして下さい'

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'mysite'
    app.config['SQLALCHEMY_DATABASE_URI'] = \
      'mysql://{user}:{password}@{host}/{db_name}?charset=utf8'.format(**{
      'user': "todo_user",
      'password': "MySQL_DB_Pass",
      'host': "localhost",
      'db_name': "ToDo_DB"
      })
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    
    from flask_todo.views import bp
    
    app.register_blueprint(bp)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    return app
