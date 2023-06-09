from application.models.base import Base
from application.models.user import User
from mongoengine import StringField, ReferenceField, DateTimeField, SequenceField, ObjectIdField, Document
from bson.objectid import ObjectId
from datetime import datetime

class Post(Document, Base):
    """
    Post Model
    {
        "msg": "Hello world",
        "user": {
            "id": "5f9f1b5b4b9b4b0b5c1b1b1b",
            "counter_id": 1,
            "username": "test"
        },
        "counter_id": 1,
        "timestamp": "2020-10-31 12:00:00"
    }
    """

    msg = StringField(required=True)
    user = ReferenceField(User)
    counter_id = SequenceField()
    timestamp = DateTimeField(default=datetime.utcnow)

    def response_mapper(self):
        """
        Returns a dictionary of key: definedKey
        """
        return {
            "id": "counter_id",
            "key": "id",
            "msg": "msg",
            "timestamp": "timestamp",
            "user": "user"
        }
