import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = 'login.login'
login_manager.login_message = 'ログインして下さい'

basedir = os.path.abspath(os.path.dirname(__name__))
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'mysite'
    app.config['SQLALCHEMY_DATABASE_URI'] = \
      'mysql://{user}:{password}@{host}/{db_name}?charset=utf8'.format(**{
      'user': "test",
      'password': "test_pass",
      'host': "localhost",
      'db_name': "testdb"
      })
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    from login.views import login_bp
    app.register_blueprint(login_bp)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    return app
