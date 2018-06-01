from flask import Flask, render_template
from jobplus.config import configs
from jobplus.models import db, User
from flask_migrate import Migrate
from flask_login import LoginManager


# create app 通过配置文件动态创建Flask app 工厂函数
def create_app(config):
    """ 根据不同的config名称,加载不同的配置 """
    app = Flask(__name__)
    app.config.from_object(configs.get(config))

    # SQLAlchemy 初始化方式 init_app
    #db.init_app(app)

    # flask_migrate 注册app
    #Migrate(app, db)

    # 扩展app注册
    register_extensions(app)

    # 工厂函数调用蓝图注册函数
    register_blueprints(app)

    return app

# 注册蓝图
def register_blueprints(app):
    from .handlers import front, admin, user
    app.register_blueprint(front)
    app.register_blueprint(admin)
    app.register_blueprint(user)

# 将Flask拓展注册到app
def register_extensions(app):
    # 初始化 sqlalchemy
    db.init_app(app)

    # flask_migrate 注册app
    Migrate(app, db)

    # 使用LoginManager类先实例化类对象
    login_manager = LoginManager()
    # 配置app
    login_manager.init_app(app)
    # 使用 login_manager.user_loader 回调函数
    @login_manager.user_loader
    def user_loader(id):
        return User.query.get(id)

    # 当用户需要登入的时候 跳转到视图的名字
    login_manager.login_view = 'front.login'

    # 未登录的用户访问login_required保护的视图时,flask_login会闪现一条消息并重定向到登录视图
    # 登录视图的名称为 login_manager.login_view
    # 当用户重定向到登入页面时的消息闪现信息
    login_manager.login_message='请登录'

    # 当用户重定向到登入页面时的消息闪现类别
    login_manager.login_message_category = 'success'
