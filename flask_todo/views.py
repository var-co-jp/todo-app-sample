from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from flask_todo.forms import LoginForm, RegisterForm, TaskForm
from flask_todo.models import User, Task
from datetime import datetime, date
from flask_todo import db

bp = Blueprint('todo_app', __name__, url_prefix='')


@bp.route('/')
def home():
    return render_template('home.html')


@bp.route('/welcome')
@login_required
def welcome():
    username = User.username
    return render_template('welcome.html', username=username)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('todo_app.home'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.select_by_email(form.email.data)
        if user and user.validate_password(form.password.data):
            login_user(user)
            next = request.args.get('next')
            if not next:
                next = url_for('todo_app.welcome')
            return redirect(next)
    return render_template('login.html', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(
            email = form.email.data,
            username = form.username.data,
            password = form.password.data
            )
        
        try:
            with db.session.begin(subtransactions=True):
                db.session.add(user)
            db.session.commit()
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()
        
        return redirect(url_for('todo_app.login'))
    return render_template('register.html', form=form)


# ユーザーページ（ここで一覧を表示する）
@bp.route('/user', methods=['GET', 'POST'])
@login_required
def user():
    form = TaskForm(request.form)
    if request.method == 'GET':
        tasks = Task.query.filter(Task.user_id == current_user.get_id()).order_by(Task.end_time).all()
    return render_template('user.html',tasks=tasks, today=date.today())
        

# 新規作成ページ
@bp.route('/create_task', methods=['GET', 'POST'])
@login_required
def create_task():
    form = TaskForm(request.form)
    if request.method == 'POST' and form.validate():        
        
        create_task = Task(
            title = form.title.data,
            detail = form.detail.data,
            end_time = form.end_time.data,
            user_id = current_user.get_id()
            )
        
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
    return render_template('create_task.html', form=form)


# 詳細ページ
@bp.route('/detail/<int:id>')
@login_required
def detail_task(id):
    task = Task.query.get(id)
    return render_template('detail.html', task=task, today=date.today())


# 削除ページ
@bp.route('/delete/<int:id>')
@login_required
def delete_task(id):
    task = Task.query.get(id)
    
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


# 更新ページ
@bp.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_task(id):
    task = Task.query.get(id)
    form = TaskForm(request.form)
    if request.method == 'GET':
        return render_template('update.html', form=form , task=task, today=date.today())
    else:
        task.title = request.form.get('title')
        task.end_time = datetime.strptime(request.form.get('end_time'), '%Y-%m-%d')
        task.detail = request.form.get('detail')
        
        update_task = Task(
            title = task.title,
            end_time = task.end_time,
            detail = task.detail
            )
        
        # update_task = Task(
        #     title = form.title.data,
        #     detail = form.detail.data,
        #     end_time = form.end_time.data
        # )
        
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()
        
        return redirect(url_for('todo_app.user'))
    