from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from flask_todo.models import User
from datetime import datetime, date
from flask_todo import db
import re

bp = Blueprint('todo_app', __name__, url_prefix='')


# 初期画面はhome.htmlを表示させます
@bp.route('/')
def home():
    return render_template('home.html')


# ToDoを表示するページを用意
@bp.route('/user')
@login_required
def user():
    return render_template('user.html')


# ユーザー登録
@bp.route('/register', methods=['GET', 'POST'])
def register():
    # 書き込まれた項目を取得する
    username = request.form.get('name')
    email = request.form.get('email')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')
    
    # メールアドレスの形式を正規表現で想定している
    pattern = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    
    # POSTリクエストの場合
    if request.method == 'POST':
        # どこかに空欄がある場合
        if username == '' or email =='' or password1 == '' or password2 == '':
            flash('空のフォームがあります')
        # パスワードが一致しない場合
        elif password1 != password2:
            flash('パスワードが一致しません')
        # メールアドレスの形式になっていない場合
        elif re.match(pattern, email) is None:
            flash('メールアドレスの形式になっていません')
        # 全て正しく入力された場合
        else:
            # 書き込まれた項目を取得する
            user = User(
                email = email,
                username = username,
                password = password1
                )
            # データベースにあるメールアドレスを取得する
            # データベースにメールアドレスが登録されていなければNoneとなる
            DBuser = User.select_by_email(email)
            
            # メールアドレスが取得された場合
            if DBuser != None:
                flash('登録済みです')
            # メールアドレスが取得されなかった場合
            else:
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
                    
                # 成功すればtodo_app.loginに遷移する
                return redirect(url_for('todo_app.login'))
    return render_template('register.html')


# ログイン
@bp.route('/login', methods=['GET', 'POST'])
def login():
    # 書き込まれた項目を取得する
    email = request.form.get('email')
    password = request.form.get('password')
    # POSTリクエストの場合
    if request.method == 'POST':
        user = User.select_by_email(email)
        # メールアドレスとパスワードが正しい場合
        if user and user.validate_password(password):
            login_user(user)
            next = request.args.get('next')
            if not next:
                next = url_for('todo_app.user')
            return redirect(next)
    return render_template('login.html', last_access=datetime.now())


# ログアウトするとtodo_app.homeに戻る
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('todo_app.home'))
