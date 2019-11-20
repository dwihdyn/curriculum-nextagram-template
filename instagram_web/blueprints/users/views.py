# basic setup
from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import current_user, login_required
from models.user import UserCredential


# aws & hybrid property setup
from instagram_web.util.helpers import upload_file_to_s3, unique_filename
from werkzeug.utils import secure_filename
from config import S3_BUCKET, S3_LOCATION
from playhouse.hybrid import hybrid_property, hybrid_method

# regex password setup
import re
from werkzeug.security import generate_password_hash


# directs this view.py to users templates
users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


# take user to sign up page
@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


# password verification & save new user data to `UserCredential` database
@users_blueprint.route('/', methods=['POST'])
def create():
    new_usr = UserCredential(
        username=request.form['username'], email=request.form['email'], password=request.form['password'], confPassword=request.form['confPassword'])

    if new_usr.password == new_usr.confPassword:

        if not UserCredential.get_or_none(email=new_usr.email):

            # regex validation
            reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
            compile_regex = re.compile(reg)
            match_pass_regex = re.search(compile_regex, new_usr.password)

            if match_pass_regex:
                # hash it
                new_usr.password = generate_password_hash(new_usr.password)
                new_usr.save()
                flash(
                    'You have successfuly signed up!. You can use your credentials to login now', 'text-success')
                return redirect(url_for('home'))
            else:
                flash('''
                password must have :
                1) a number
                2) an uppercase & lowercase
                3) a special symbol (!,@,#,..)
                4) length 6 to 20 char
                ''', 'text-danger')
                return render_template('users/new.html')

        else:
            flash('This email has already been taken', 'text-danger')
            return render_template('users/new.html')

    else:
        flash('Password and confirm password dont match', 'text-danger')
        return render_template('users/new.html')


# show selected user profile page
@users_blueprint.route('/<user_detail>', methods=["GET"])
@login_required
def show(user_detail):
    # selected_user return the details of current user (username, email, password, profile pic)
    selected_user = UserCredential.get_or_none(
        UserCredential.username == user_detail)
    if not selected_user:
        flash(
            f"User with username {user_detail} does not exist!", 'text-warning')
        return redirect(url_for('home'))

    return render_template('users/show.html', user_detail=selected_user)

# =======================================================================================
@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


# settings : to change user details
@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    return render_template('users/edit.html')


# accept input from user, and save it | once user entered edited data from edit.html , go to this function to made the changes
@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    ongoing_user = UserCredential.get_by_id(id)
    ongoing_user.name = request.form.get('new_username')
    ongoing_user.email = request.form.get('new_email')
    if ongoing_user.save():
        flash('Information successfully updated', 'text-success')
        return redirect(url_for('home'))
    else:
        for i in ongoing_user.errors:
            flash(i, 'text-danger')
            return render_template('users/edit.html')


# uploading picture to aws
@users_blueprint.route('/<id>/profile_image', methods=['POST'])
@login_required
def profile_image(id):

    # 'profie_image' refers to `input` name in users/edit.html | if no image uploaded, give warning
    if 'profile_image' not in request.files:
        flash('Please choose your profile picture to be uploaded !', 'text-warning')
        return redirect(url_for('users.edit', id=current_user.id))

    # receive file from user (same idea as `request.form.get('username')` in UserCredential)
    file = request.files['profile_image']

    # if provided file is not image file, give warning
    if not file or file.filename == "":
        flash('Please provide a valid file !', 'text-warning')
        return redirect(url_for('users.edit', id=current_user.id))

    # add timestamp to part of the .jpg name
    file.filename = unique_filename(file)

    # upload picture to given userId, and save it in string form in database. how we call the image is setup in models.user.py `S3_LOCATION + imageName.jpg`
    uploaded_pic = upload_file_to_s3(file, S3_BUCKET)
    ongoing_user = UserCredential.get_by_id(id)
    ongoing_user.profile_image = uploaded_pic
    ongoing_user.save()

    # if image did not uploaded to AWS, give warning
    if not uploaded_pic:
        flash('There are issue in uploading the picture to server (AWS), should be okay now. try again!', 'text-danger')
        return redirect(url_for('users.edit', id=current_user.id))

    # when all if are passed, tell user that picture are successfully uploaded
    flash('Profile image are successfully uploaded!', 'text-success')
    return redirect(url_for('home'))
