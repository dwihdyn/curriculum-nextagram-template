from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required

from instagram_web.util.braintree import generate_client_token, complete_transaction

from models.image import ImageFeed


donations_blueprint = Blueprint(
    'donations', __name__, template_folder='templates')


# generate braintree token for selected image to donate
@donations_blueprint.route('/<image_id>/new', methods=['GET'])
@login_required
def new(image_id):
    image = ImageFeed.get_or_none(
        ImageFeed.id == image_id)  # return the image_id if true, return None if false
    client_token = generate_client_token

    if not image:
        flash('Unable to find image with provided id!', 'text-warning')
        return redirect(url_for('home'))

    # same name to ensure no type
    return render_template('donations/new.html', image=image, client_token=client_token)


@donations_blueprint.route('/create', methods=['POST'])
@login_required
def create():
    pass