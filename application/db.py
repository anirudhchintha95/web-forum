"""
This file contains the DB class which is used to connect to the database and
return a collection object.
"""
from mongoengine import connect


class DB:
    """
    DB class
    """

    def __init__(self, mongo_uri, db_name):
        self.mongo_uri = mongo_uri
        self.database_name = db_name
        self.client = None
        self.database = None

    def connect(self):
        """
        Connect to the database
        """
        self.client = connect(db=self.database_name, host=self.mongo_uri)
        self.database = self.client[self.database_name]

    def disconnect(self):
        """
        Disconnect from the database
        """
        self.client.close()

    def get_collection(self, collection_name):
        """
        Get a collection object
        """
        if collection_name not in self.database.list_collection_names():
            self.database.create_collection(collection_name)
        return self.database[collection_name]

    def get_db(self):
        """
        Get the database object
        """
        return self.database

    def get_collection_names(self):
        """
        Get the collection names
        """
        return self.get_db().list_collection_names()
