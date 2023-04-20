"""
Models Module for Web Forum Application
"""
from datetime import datetime
from mongoengine import (
    Document,
    StringField,
    ReferenceField,
    DateTimeField,
    SequenceField,
)

class CounterIdMixin:
    """
    Mixin for counter
    """

    @classmethod
    def get_by_counter_id(cls, counter_id):
        """
        Returns a document by counter id
        """
        return cls.objects(counter_id=counter_id).first()
    

class ResponseMixin:
    """
    Mixin for response mapping
    """

    def response_mapper(self):
        """
        Returns a dictionary of key: definedKey
        """
        raise NotImplementedError("response_mapper not implemented")

    def to_response(self):
        """
        Returns a dictionary of key: value
        """
        return {
            f"{key}": self[definedKey] for key, definedKey in self.response_mapper()
        }


class User(Document, ResponseMixin, CounterIdMixin):
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
    counter_id = SequenceField()
    timestamp = DateTimeField(default=datetime.now)

    def response_mapper(self):
        """
        Returns a dictionary of key: definedKey
        """
        return {
            "username": "username",
            "id": "counter_id",
            "key": "_id",
            "timestamp": "timestamp",
        }


class Post(Document, ResponseMixin, CounterIdMixin):
    """
    Post Model
    {
        "msg": "Hello world",
        "user": {
            "_id": "5f9f1b5b4b9b4b0b5c1b1b1b",
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
    timestamp = DateTimeField(default=datetime.now)

    def response_mapper(self):
        """
        Returns a dictionary of key: definedKey
        """
        return {
            "user": "user",
            "id": "counter_id",
            "key": "_id",
            "msg": "msg",
            "timestamp": "timestamp",
        }
