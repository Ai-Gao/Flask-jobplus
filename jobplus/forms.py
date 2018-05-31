#coding='utf-8'

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, URL, NumberRange

# 注册表单
class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(message='用户名不能为空'), Length(3,24, message='用户名长度要在3~24个字符之间')])
    email = StringField('邮箱', validators=[DataRequired(message='邮箱不能为空'), Email(message='请输入合法的email地址')])
    password = PasswordField('密码', validators=[DataRequired(message='密码不能为空'), Length(6,24, message='密码长度要在6~24个字符之间')])
    repeat_password = PasswordField('重复密码', validators=[DataRequired(message='密码不能为空'), EqualTo('password', message='密码要相等')])
    submit = SubmitField('提交')

# 登录表单
class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(message='用户名不能为空'), Length(3,24, message='用户名长度要在3~24个字符之间')])
    #email = StringField('邮箱', validators=[DataRequired(message='邮箱不能为空'), Email(message='请输入合法的邮箱')])
    password = PasswordField('密码', validators=[DataRequired(message='密码不能为空'), Length(6,24, message='密码长度要在6~24个字符之间')])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')

