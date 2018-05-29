from flask import Flask, render_template
from jobplus.config import configs
from jobplus.models import db
from flask_migrate import Migrate

# create app 通过配置文件动态创建Flask app 工厂函数
def create_app(config):
    """ 根据不同的config名称,加载不同的配置 """
    app = Flask(__name__)
    app.config.from_object(configs.get(config))

    # SQLAlchemy 初始化方式 init_app
    db.init_app(app)

    # flask_migrate 注册app
    Migrate(app, db)

    # 工厂函数调用蓝图注册函数
    register_blueprints(app)

    return app

# 注册蓝图
def register_blueprints(app):
    from .handlers import front, admin, user
    app.register_blueprint(front)
    app.register_blueprint(admin)
    app.register_blueprint(user)

