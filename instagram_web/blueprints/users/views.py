from flask import Blueprint, render_template, request, url_for, redirect, flash
from models.user import *


# directs this view.py to users templates
users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')

# == SIGNUP ==
# take user to enter signup data
@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


# once user type their data & press submit, go here (backend setup)
@users_blueprint.route('/', methods=['POST'])
def create():
    new_usr = UserCredential(
        name=request.form['username'], email=request.form['email'], password=request.form['password'], confPassword=request.form['confPassword'])
    # indent properly when uncomment. Below is password validation

    if new_usr.password == new_usr.confPassword:
        # breakpoint()
        if not UserCredential.get_or_none(email=new_usr.email):

            new_usr.save()
            if not new_usr.errors:
                flash(
                    'You have successfuly signed up!. You can use your credentials to login now', 'text-success')
                return redirect(url_for('home'))
            else:
                for i in new_usr.errors:
                    flash(i, 'text-danger')
                return render_template('users/new.html')

        else:
            flash('This email has already been taken', 'text-danger')
            return render_template('users/new.html')

    else:
        flash('Password and confirm password dont match', 'text-danger')
        return render_template('users/new.html')


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
