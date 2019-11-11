from flask import Blueprint, render_template, request, url_for, redirect, flash
from models.user import *
from werkzeug.security import check_password_hash

sessions_blueprint = Blueprint(
    'sessions', __name__, template_folder='templates')


# new() session when use login
@sessions_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('sessions/new.html')


# create() new session
@sessions_blueprint.route('/', methods=['POST'])
def create():
    enterred_username = request.form.get('username')
    enterred_password = request.form.get('password')
    user_check = UserCredential.get_or_none(name=enterred_username)
    if user_check:
        pass_check = check_password_hash(
            user_check.password, enterred_password)
        if pass_check:
            return redirect(url_for('sessions.show', user_name=enterred_username))
        else:
            flash('Invalid username or password (or both)', 'text-danger')
            return render_template('sessions/new.html')
    else:
        flash('User does not exist', 'text-danger')
        return render_template('sessions/new.html')

    # return redirect(url_for('home'))


@sessions_blueprint.route('/<user_name>')
def show(user_name):
    return render_template("home.html", username_profile_page=user_name)

# secret key for ?
