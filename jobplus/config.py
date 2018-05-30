class BaseConfig(object):
    """ 配置基类 """
    SECRET_KEY = 'secret key'

class DevelopmentConfig(BaseConfig):
    """ 开发环境配置 """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:123@localhost:3306/jobplus?charset=utf8'

class ProductionConfig(BaseConfig):
    pass

class TestingConfig(BaseConfig):
    """ 测试环境配置 """
    pass

configs={
        'development' : DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig
        }


