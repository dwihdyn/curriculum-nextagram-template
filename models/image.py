from models.base_model import BaseModel
import peewee as pw
from models.user import UserCredential

# for hybrid property -> image uploading to combine the image name + S3_LOCATION address
from playhouse.hybrid import hybrid_property
from config import S3_LOCATION


class ImageFeed(BaseModel):
    user_id = pw.ForeignKeyField(
        UserCredential, backref="images_feed")  # logged_in_user
    picture_name = pw.CharField(null=False)
    caption = pw.CharField(null=False)

    @hybrid_property  # full_image_url
    def full_newpost_url(self):
        return S3_LOCATION + self.picture_name
