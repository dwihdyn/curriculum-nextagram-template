from flask import Blueprint, render_template
from flask_login import login_required

# from instagram_web.util.braintree import


donations_blueprint = Blueprint(
    'donations', __name__, template_folder='templates')


# generate braintree token for selected image to donate
@donations_blueprint.route('/new', methods=['GET'])
@login_required
def new():
    return render_template('donations/new.html')


@donations_blueprint.route
