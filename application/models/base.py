from datetime import datetime
from bson import json_util, ObjectId
import json
from mongoengine import DateTimeField, SequenceField, Document


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

    def get_value(self, key):
        """
        Returns the value of the key
        """
        if isinstance(self[key], ObjectId):
            return str(self[key])
        
        return self[key]

    def to_response(self):
        """
        Returns a dictionary of key: value
        """
        data = {
            key: self.get_value(definedKey)
            for key, definedKey in self.response_mapper().items()
        }

        return json.loads(json_util.dumps(data))


class Base(Document, ResponseMixin, CounterIdMixin):
    timestamp = DateTimeField(default=datetime.now)
    counter_id = SequenceField()

    meta = {"allow_inheritance": True}
