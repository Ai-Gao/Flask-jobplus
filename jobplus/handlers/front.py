from flask import Blueprint, render_template, redirect
from jobplus.forms import RegisterForm, LoginForm
from flask_login import login_user, logout_user, login_required
from jobplus.models import db, User, Job
from flask import flash



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
        # 通过用户名登录
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user, form.remember_me.data)
        flash('登录成功', 'success')
        return redirect(url_for('.index'))
    return render_template('login.html', form=form)

# 首页 登出路由
@front.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已退出登录', 'success')
    return redirect(url_for('front.index'))

# 首页 用户注册路由
@front.route('/userregister', methods=['POST', 'GET'])
def userregister():
    form = RegisterForm()
    if form.validate_on_submit():
        form.create_user()
        flash('注册成功,请登录', 'success')
        return redirect(url_for('front.login'))
    return render_template('userregister.html', form=form)

# 首页 公司注册路由
@front.route('/companyregister', methods=['POST','GET'])
def companyregister():
    form = RegisterForm()
    form.name.label= u'企业名称'
    if form.validate_on_submit():
        company_user = form.create_user()
        company_user.role = User.ROLE_COMPANY
        db.session.add(company_user)
        db.session.commit()
        flash('注册成功,请登录', 'success')
        return redirect(url_for('front.login'))
    return render_template('companyregister.html', form=form)

