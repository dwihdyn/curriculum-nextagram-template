# all databases

# import re
from models.base_model import BaseModel
import peewee as pw
# from werkzeug.security import generate_password_hash
from flask_login import UserMixin

# for hybrid property -> image uploading to combine the image name + S3_LOCATION address
from playhouse.hybrid import hybrid_property
from config import S3_LOCATION


class UserCredential(UserMixin, BaseModel):
    name = pw.CharField(unique=False)
    email = pw.CharField()
    password = pw.CharField()
    profile_image = pw.CharField(default='1573637551default-pic.jpg')

    # below is hybrid/shortcut version of `profile_image_url = pw.Charfield()` and enter both names in it
    @hybrid_property
    def profile_image_url(self):
        return S3_LOCATION + self.profile_image
