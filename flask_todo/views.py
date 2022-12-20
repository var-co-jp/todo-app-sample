from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from flask_todo.models import User, Task
from datetime import datetime, date
from flask_todo import db
import re

bp = Blueprint('todo_app', __name__, url_prefix='')


# 初期画面はhome.htmlを表示させます
@bp.route('/')
def home():
    return render_template('home.html')


# ログアウトするとhome.htmlに戻る
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('todo_app.home'))


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
                    
                # 成功すればlogin.htmlに遷移する
                return redirect(url_for('todo_app.login'))
    return render_template('register.html')


# タスク一覧
@bp.route('/user', methods=['GET', 'POST'])
# ログインできている時に処理を実行できる
@login_required
def user():
    # GETリクエストの場合
    if request.method == 'GET':
        # 現在ログインしている人のタスクをタスク終了日が早い順に全て取得する
        tasks = Task.query.filter(Task.user_id == current_user.get_id()).order_by(Task.end_time).all()
    return render_template('user.html',tasks=tasks, today=date.today())
    
        
# 新規タスク作成
@bp.route('/create_task', methods=['GET', 'POST'])
# ログインできている時に処理を実行できる
@login_required
def create_task():
    # POSTリクエストの場合
    if request.method == 'POST':        
        # 書き込まれた項目を取得する
        title = request.form.get('title')
        detail = request.form.get('detail')
        end_time = datetime.strptime(request.form.get('end_time'), '%Y-%m-%d')
        
        # どこかに空欄がある場合
        if title == '' or detail =='' or end_time == '':
            flash('空のフォームがあります')
		# 全て正しく入力された場合
        else:
            # 取得した項目をデータベースのカラム名に紐付ける
            create_task = Task(
                title = title,
                end_time = end_time,
                detail = detail,
                user_id = current_user.get_id()
                )
            
            # データベースへの書き込み（Create処理）
            try:
                with db.session.begin(subtransactions=True):
                    db.session.add(create_task)
                db.session.commit()
            except:
                db.session.rollback()
                raise
            finally:
                db.session.close()
                
            return redirect(url_for('todo_app.user'))
    return render_template('create_task.html')


# タスク詳細
@bp.route('/detail/<int:id>')
# ログインできている時に処理を実行できる
@login_required
def detail_task(id):
    # 選択したタスクの情報を取得（Read処理）
    task = Task.query.get(id)
    return render_template('detail.html', task=task, today=date.today())


# タスク削除
@bp.route('/delete/<int:id>')
# ログインできている時に処理を実行できる
@login_required
def delete_task(id):
    # 選択したタスクの情報を取得
    task = Task.query.get(id)
    
    # データベースへの書き込み（Delete処理）
    try:
        with db.session.begin(subtransactions=True):
            db.session.delete(task)
        db.session.commit()
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()
        
    return redirect(url_for('todo_app.user'))


# タスク更新
@bp.route('/update/<int:id>', methods=['GET', 'POST'])
# ログインできている時に処理を実行できる
@login_required
def update_task(id):
    # 選択したタスクの情報を取得
    task = Task.query.get(id)
    
    # GETリクエストの場合
    if request.method == 'GET':
        return render_template('update.html', task=task, today=date.today())
    # POSTリクエストの場合
    else:
        task.title = request.form.get('title')
        task.end_time = datetime.strptime(request.form.get('end_time'), '%Y-%m-%d')
        task.detail = request.form.get('detail')
        
        update_task = Task(
            title = task.title,
            end_time = task.end_time,
            detail = task.detail
            )
        
        # データベースへの書き込み（Update処理）
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()
        
        return redirect(url_for('todo_app.user'))
    