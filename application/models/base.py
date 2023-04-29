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

    def get_value(self, key, remove_unique_key):
        """
        Returns the value of the key
        """
        if isinstance(self[key], ObjectId):
            return str(self[key])
        
        if key == 'timestamp':
            return self[key].isoformat()
        if key == "user" and self[key] is not None:
            return self[key].to_response(remove_unique_key)
    
        return self[key]

    def to_response(self, remove_unique_key=None):
        """
        Returns a dictionary of key: value
        """
        data = {
            key: self.get_value(definedKey, remove_unique_key)
            for key, definedKey in self.response_mapper().items()
            if key != "key" or not remove_unique_key
        }

        return json.loads(json_util.dumps(data))


class Base(ResponseMixin, CounterIdMixin):
    pass
