from flask import Blueprint, jsonify
from models.user import UserCredential
from models.image import ImageFeed

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
@users_api_blueprint.route('/show', methods=['GET'])
def show():
    all_users = UserCredential.select().prefetch(ImageFeed)
    # resp = [
    #     {
    #         "id": i.id,
    #         "username": i.username,
    #         "profileImage": i.profile_image_url
    #     }   
    #     for i in all_users
    # ]

    resp = []
    for i in all_users:
        resp.append(        {
            "id": i.id,
            "username": i.username,
            "profileImage": i.profile_image_url
        }) 





    return jsonify(resp)
