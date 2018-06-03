#coding='utf-8'

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, URL, NumberRange
from jobplus.models import db, User
from wtforms import ValidationError

# 注册表单
class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(message='用户名不能为空'), Length(3,24, message='用户名长度要在3~24个字符之间')])
    email = StringField('邮箱', validators=[DataRequired(message='邮箱不能为空'), Email(message='请输入合法的email地址')])
    password = PasswordField('密码', validators=[DataRequired(message='密码不能为空'), Length(6,24, message='密码长度要在6~24个字符之间')])
    repeat_password = PasswordField('重复密码', validators=[DataRequired(message='密码不能为空'), EqualTo('password', message='密码要相等')])
    submit = SubmitField('提交')

    # 自定义表单数据验证器(固定格式) 注册时用户名验证
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经存在')

    # 自定义表单数据验证器 注册时邮箱验证
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经存在')

    # 实现注册功能 (添加表单数据到数据库)

    def create_user(self):
        user = User()
        user.username = self.username.data
        user.email = self.email.data
        user.password = self.password.data
        db.session.add(user)
        db.session.commit()
        return user

# 登录表单
class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(message='用户名不能为空'), Length(3,24, message='用户名长度要在3~24个字符之间')])
    #email = StringField('邮箱', validators=[DataRequired(message='邮箱不能为空'), Email(message='请输入合法的邮箱')])
    password = PasswordField('密码', validators=[DataRequired(message='密码不能为空'), Length(6,24, message='密码长度要在6~24个字符之间')])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')

    # 自定义表单数据验证器 登录时用户名验证
    def validate_username(self, field):
        if field.data and not User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名未注册')

    # 自定义表单数据验证器 登录时密码验证
    def validate_password(self, field):
        user = User.query.filter_by(username=self.username.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('密码错误')

# 求职者个人信息配置表单
class UserProfileForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(message='用户名不能为空'), Length(3,24, message='用户名长度要在3~24个字符之间')])
    email=StringField('邮箱', validators=[DataRequired(message='邮箱不能为空'), Email(message='请输入合法的邮箱')])
    password = PasswordField('密码', validators=[DataRequired(message='密码不能为空')])
    phone = StringField('手机号', validators=[DataRequired(message='手机号不能为空'), NumberRange(min=11)])

