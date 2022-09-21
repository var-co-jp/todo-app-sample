from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_user, login_required, logout_user
from flask_todo.forms import LoginForm, RegisterForm
from flask_todo.models import User, Task
from datetime import datetime

bp = Blueprint('todo_app', __name__, url_prefix='')

@bp.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        tasks = Task.query.all()
        return render_template('home.html', tasks=tasks)

    else:
        title = request.form.get('title')
        detail = request.form.get('detail')
        due = request.form.get('due')
        
        due = datetime.strptime(due, '%Y-%m-%d')
        new_task = Task(title=title, detail=detail, due=due)

        db.session.add(new_task)
        db.session.commit()
        return redirect('/')
    # return render_template('home.html')

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
        user.add_user()
        return redirect(url_for('todo_app.login'))
    return render_template('register.html', form=form)

@bp.route('/user')
@login_required
def user():
    return render_template('user.html')

@bp.route('/create')
def create():
    return render_template('create.html')