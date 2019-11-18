from models.base_model import BaseModel
import peewee as pw

# since we want to know the donation is given to which particular picture, from a particular user, it need to be connected with `UserCredential` & `ImageFeed` table
from models.user import UserCredential
from models.image import ImageFeed


class Donation(BaseModel):
    user_id = pw.ForeignKeyField(UserCredential, backref="donations")
    image_id = pw.ForeignKeyField(ImageFeed, backref="donations")
    amount = pw.DecimalField(null=False, decimal_places=2)
