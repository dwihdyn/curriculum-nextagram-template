from app import app
from flask import render_template
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.images.views import images_blueprint
from instagram_web.blueprints.donations.views import donations_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles

# used to solve `n+1 query`, and pass python code to home.html as `all_users`
from models.image import ImageFeed
from models.user import UserCredential


# gmail OAuth
from instagram_web.util.google_oauth import oauth

assets = Environment(app)
assets.register(bundles)

# gmail OAuth initialise
oauth.init_app(app)


# for user handling
app.register_blueprint(users_blueprint, url_prefix="/users")

# EXCLUSIVELY just for login & logout process ONLY
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")

# user feed handler
app.register_blueprint(images_blueprint, url_prefix="/images")

# donation handler
app.register_blueprint(donations_blueprint, url_prefix="/donations")


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route("/")
def home():
    # return render_template('home.html', img_feed=ImageFeed)
    # `img_feed` is to call out users images with 2 queries only (and not `n users + 1` query)
    return render_template('home.html', all_users=UserCredential.select().prefetch(ImageFeed))
