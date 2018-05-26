from flask import Blueprint, render_template

# 省略url_prefix 默认为 /
front = Blueprint('front', __name__)

@front.route('/')
def index():
    return render_template('index.html')

