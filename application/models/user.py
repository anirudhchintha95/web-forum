from application.models.base import Base
from mongoengine import StringField
from werkzeug.security import generate_password_hash, check_password_hash


class User(Base):
    """
    User Model
    {
        "username": "test",
        "password": "test",
        "counter": 1,
        "timestamp": "2020-10-31 12:00:00"
    }
    """

    username = StringField(required=True)
    password = StringField(required=True, min_length=8)

    @classmethod
    def init_for_create(cls, username, password):
        """
        Initializes a user and hashes the password
        """
        user = cls(username=username)
        user.hash_password(password)
        return user

    def response_mapper(self):
        """
        Returns a dictionary of key: definedKey
        """
        return {
            "username": "username",
            "id": "counter_id",
            "key": "id",
            "timestamp": "timestamp",
        }

    def hash_password(self, raw_password):
        """
        Hashes the password
        """
        self.password = generate_password_hash(raw_password)
        return self

    def check_password(self, raw_password):
        """
        Checks if the password passed is user's password
        """
        return check_password_hash(raw_password, self.password)
