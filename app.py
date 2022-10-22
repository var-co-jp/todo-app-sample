from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

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

db.create_all(app)
db.init_app(app)
migrate.init_app(app, db)

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    
    
    def __init__(self, username):
        self.username = username
    
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


@app.route('/')
def hello():
    
    return '<h1>Hello World</h1>'

if __name__ == "__main__":
    app.run()