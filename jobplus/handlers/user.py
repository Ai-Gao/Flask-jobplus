from flask import Blueprint, render_template
from flask_login import login_required
from jobplus.forms import UserProfileForm

user = Blueprint('user', __name__, url_prefix='/user')

@user.route('/profile', methods=['POST', 'GET'])
@login_required
def user_profile():
    form = UserProfileForm()
    return render_template('user/profile.html', form=form)

