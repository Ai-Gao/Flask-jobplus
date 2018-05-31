from flask import Blueprint, render_template, redirect
from jobplus.forms import RegisterForm, LoginForm
from flask_login import login_user

# 省略url_prefix 默认为 /
front = Blueprint('front', __name__)

@front.route('/')
def index():
    return render_template('index.html')

# 首页 登录路由
@front.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user, form.remember_me.data)
        return redirect(url_for('.index'))
    return render_template('login.html', form=form)

# 首页 注册路由
@front.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    return render_template('register.html', form=form)

