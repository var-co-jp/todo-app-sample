from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from flask_todo.forms import LoginForm, RegisterForm, TaskForm
from flask_todo.models import User, Task
from datetime import datetime
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
        user.add_user_db()
        return redirect(url_for('todo_app.login'))
    return render_template('register.html', form=form)


# ユーザーページ（ここで一覧を表示する）
@bp.route('/user', methods=['GET', 'POST'])
@login_required
def user():
    form = TaskForm(request.form)
    if request.method == 'GET':
        tasks = Task.query.order_by(Task.due).all()
    return render_template('user.html',tasks=tasks)
        

# 新規作成ページ
@bp.route('/create_task', methods=['GET', 'POST'])
@login_required
def create_task():
    form = TaskForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        detail = form.detail.data
        due = form.due.data
        
        create_task = Task(
            title = title,
            detail = detail,
            due = due
            )
        
        create_task.add_task_db()        
        return redirect(url_for('todo_app.user'))
    return render_template('create_task.html', form=form)


# 詳細ページ
@bp.route('/detail/<int:id>')
@login_required
def detail_task(id):
    task = Task.query.get(id)
    return render_template('detail.html', task=task)


# 削除ページ
@bp.route('/delete/<int:id>')
@login_required
def delete_task(id):
    task = Task.query.get(id)
    task.delete_task_db()
    return redirect(url_for('todo_app.user'))


# 更新ページ
@bp.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_task(id):
    task = Task.query.get(id)
    if request.method == 'GET':
        return render_template('update.html', task=task)
    else:
        task.title = request.form.get('title'),
        task.due = datetime.strptime(request.form.get('due'), '%Y-%m-%d'),
        task.detail = request.form.get('detail')
        
        update_task = Task(
            title = task.title,
            due = task.due,
            detail = task.detail
            )
        
        update_task.edit_task_db()
        return redirect(url_for('todo_app.user'))
    