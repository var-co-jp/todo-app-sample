from wtforms.form import Form
from wtforms.fields import StringField, PasswordField, SubmitField, TextAreaField, DateField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_todo.models import User, Task


class LoginForm(Form):
    email = StringField('メール: ', validators=[DataRequired(), Email()])
    password = PasswordField('パスワード: ', validators=[DataRequired()])
    submit = SubmitField('ログイン')


class RegisterForm(Form):
    email = StringField('メール： ', validators=[DataRequired(), Email()])
    username = StringField('名前： ', validators=[DataRequired()])
    password = PasswordField(
        'パスワード： ', validators=[DataRequired(), EqualTo('password_confirm', message='パスワードが一致しません')]
    )
    password_confirm = PasswordField('パスワード確認', validators=[DataRequired()])
    submit = SubmitField('登録')
    
    def validate_email(self, field):
        if User.select_by_email(field.data):
            raise ValidationError('メールアドレスは既に登録されています')
        
        
class TaskForm(Form):
    title = StringField('タイトル： ', validators=[DataRequired()])
    due = DateField('日付:', validators=[DataRequired()], format='%Y-%m-%d')
    detail = TextAreaField('詳細： ', validators=[DataRequired()])
    submit = SubmitField('登録')
