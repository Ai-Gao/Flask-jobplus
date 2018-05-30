from flask import Blueprint, render_template

# 省略url_prefix 默认为 /
front = Blueprint('front', __name__)

@front.route('/')
def index():
    return render_template('index.html')

# 首页 登录路由
@front.route('/login', methods=['POST', 'GET'])
def login():
    return render_template('login.html')

# 首页 注册路由
@front.route('/register', methods=['POST', 'GET'])
def register():
    return render_template('register.html')

