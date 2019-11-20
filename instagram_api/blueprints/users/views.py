from flask import Blueprint, jsonify
from models.user import UserCredential

# # JWT : JSON Web Token handle login part of our UserCredential database | jwt_required same as login_required
# from flask_jwt import jwt_required


users_api_blueprint = Blueprint('users_api',
                                __name__,
                                template_folder='templates')


@users_api_blueprint.route('/', methods=['GET'])
def index():
    return "USERS API"


# usually we render HTML in flask using `return render_template('home.html')`
# in API, we return JSON. how ? by using jsonify to convert from our python code to JSON
@users_api_blueprint.route('/<username>', methods=['GET'])
def show(username):
    user = UserCredential.get_or_none(UserCredential.username == username)

    if not user:
        # return result in JSON format, converted using jsonify
        resp = {
            'message': 'No user found with that given username',
            'status': 404
        }
        return jsonify(resp)

    resp = {
        'message': 'User found!, showing the user info',
        'status': 200,
        'data': [{
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'profileImg': user.profile_image_url
        }]
    }
    return jsonify(resp)
