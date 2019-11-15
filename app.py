import os
import config
from flask import Flask
from models.base_model import db
from models.user import UserCredential
import peeweedbevolve

# CSRF attack protection
from flask_wtf.csrf import CSRFProtect

# persistent login user setup
from flask_login import LoginManager

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'instagram_web')

app = Flask('NEXTAGRAM', root_path=web_dir)


# protection
csrf = CSRFProtect(app)

# login setup
login_manager = LoginManager()
login_manager.init_app(app)


if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")


@app.before_request
def before_request():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc

# login setup | load all of the user database using peewee method. and pull that one user.id out to be shown in homepage
@login_manager.user_loader
def load_user(selected_user_id):
    return UserCredential.get(UserCredential.id == selected_user_id)
