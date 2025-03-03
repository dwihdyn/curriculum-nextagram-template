from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from instagram_web.util.braintree import generate_client_token, complete_transaction

from models.image import ImageFeed
from models.donation import Donation


donations_blueprint = Blueprint(
    'donations', __name__, template_folder='templates')


# generate braintree token for selected image to donate
@donations_blueprint.route('/<image_id>/new', methods=['GET'])
@login_required
def new(image_id):
    # image & client_token to pass it to home.html
    image = ImageFeed.get_or_none(
        ImageFeed.id == image_id)  # return the image_id if true, return None if false
    client_token = generate_client_token()

    # if not image:
    #     flash('Unable to find image with provided id!', 'text-warning')
    #     return redirect(url_for('home'))

    # # same name to ensure no type
    return render_template('donations/new.html', image=image, client_token=client_token)


# validation that user has typed in donated amount + handle donation request
@donations_blueprint.route('/<image_id>/create', methods=['POST'])
@login_required
def create(image_id):
    amount = request.form.get('donation_amount')
    image = ImageFeed.get_or_none(ImageFeed.id == image_id)

    if not amount or not round(int(amount)) > 0:
        flash('Please specify the amount of money to be donated', 'text-warning')
        return redirect(url_for('donations.new', image_id=image.id))

    # submit payment to braintree server first, and then save it local (to avoid scenario that we successfuly save local, but fail in braintree server, we must delete the local one first)

    # submit donation to braintree server
    # `nonce_from_the_client` taking token from frontend (new.html) to backend (here views.py)
    nonce_from_the_client = request.form["payment_method_nonce"]
    send_donation_to_braintree = complete_transaction(
        nonce_from_the_client, amount)
    if not send_donation_to_braintree:
        flash('Something wrong with braintree server, please try again', 'text-warning')
        return redirect(url_for('donations.new', image_id=image.id))

    # submit donation to your psql local server
    new_donation = Donation(
        user_id=current_user.id,
        image_id=image.id,
        amount=amount
    )
    new_donation.save()

    if not new_donation:
        flash('Something went wrong with your psql local server, please try again', 'text-warning')
        return redirect(url_for('donations.new', image_id=image.id))

    flash(
        f"Donation to {image.user_id.username} of USD {amount} is successful!", 'text-success')
    return redirect(url_for('home'))
