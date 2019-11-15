from flask import Blueprint, render_template, request, url_for, redirect, flash
from models.user import *
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required, current_user


from instagram_web.util.google_oauth import oauth


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
    # breakpoint()
    if user_check:
        pass_check = check_password_hash(
            user_check.password, enterred_password)
        if pass_check:
            # login here
            login_user(user_check)

            # return redirect(url_for('users.show', username=enterred_username))
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password (or both)', 'text-danger')
            return render_template('sessions/new.html')
    else:
        flash('User does not exist', 'text-danger')
        return render_template('sessions/new.html')

    # return redirect(url_for('home'))


# @sessions_blueprint.route('/<user_name>')
# def show(user_name):
#     return render_template("home.html", username_profile_page=user_name)


# logout is to DESTROY the current session
@sessions_blueprint.route('/delete')  # methods=['POST']
@login_required   # upon loggin out, need to make sure that user HAS to login first, hence `login_required` from `flask-login` package is needed
def destroy():
    # breakpoint()
    logout_user()
    flash('You have successfully logged out', 'text-success')
    return redirect(url_for('sessions.new'))


# gmail OAuth : take client (user) from our nextagram to google auth
@sessions_blueprint.route('/login/google', methods=['GET'])
def google_login():
    # below using url_for to make it dynamic, ensure still works when we go live (not localhost:5000 anymore)
    redirect_uri = url_for('sessions.authorize_google', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


# what to do after user click which gmail to login
@sessions_blueprint.route('/authorize/google', methods=['GET'])
def authorize_google():
    token = oauth.google.authorize_access_token()
    if not token:
        flash('Opps, something went wrong, try again', 'text-danger')
        return redirect(url_for('sessions.new'))

    email = oauth.google.get(
        'https://www.googleapis.com/oauth2/v2/userinfo').json()['email']

    user = UserCredential.get_or_none(UserCredential.email == email)

    if not user:
        flash('no such email have registered!', 'text-danger')
        return redirect(url_for('sessions.new'))

    flash('Welcome back!', 'text-success')
    login_user(user)
    return redirect(url_for('home'))
