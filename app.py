from flask import Flask, request, render_template, redirect, url_for
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


db.init_app(app)
migrate.init_app(app, db)


# Userテーブルの定義
class User(db.Model):
    # テーブル名を設定
    __tablename__ = 'users'
    
    # カラムを定義
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    
    def __init__(self, username):
        self.username = username

# データベースに書き込むためのロジック
@app.route('/', methods=['GET', 'POST'])
def write_db():
    # POSTリクエストの場合
    if request.method == 'POST':
        # 書き込まれた項目を取得する
        username = request.form.get('username')
        
        # 取得した項目をデータベースのカラム名に紐付ける
        user = User(
            username = username
            )
        
        # データベースへの書き込みを行う
        try:
            # データベースとの接続を開始する
            with db.session.begin(subtransactions=True):
                # データベースに書き込むデータを用意する
                db.session.add(user)
            # データベースへの書き込みを実行する
            db.session.commit()
        # 書き込みがうまくいかない場合
        except:
            # データベースへの書き込みを行わずにロールバックする
            db.session.rollback()
            raise
        # データベースとの接続を終了する
        finally:
            db.session.close()
            
        # 成功すればread_dbに遷移する
        return redirect(url_for('read_db'))
    return render_template('insert.html')

# データベースから読み込むためのロジック
@app.route('/read_db')
def read_db():
    # Userテーブルのidを降順で並べて１番最初のデータ取得する
    users = db.session.query(User).order_by(User.id.desc()).first()
    return render_template('user.html', users=users)

if __name__ == "__main__":
    app.run(debug=True)