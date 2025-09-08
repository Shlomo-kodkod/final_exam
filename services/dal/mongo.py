from pymongo import MongoClient
from services.utils.utils import setup_logger


class Mongo:
    _instance = None
    _initialized = False

    def __new__(cls, uri):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, uri):
        if Mongo._initialized:
            return
        self.__logger = setup_logger("DAL")
        self.__uri = uri
        self.__client = None
        self.__db = None
        Mongo._initialized = True

    def connect(self, db: str):
        """
        Connect to the mongo database.
        """
        if self.__db is not None:
            self.__logger.info("Already connected to MongoDB")
            return
        try:
            uri = self.__uri
            self.__client = MongoClient(uri)
            self.__db = self.__client[db]
            self.__logger.info(f"Connected to MongoDB database: {db}")
        except Exception as e:
            self.__logger.error(f"Failed to connect to MongoDB: {e}")
            raise e

    def disconnect(self):
        """
        Disconnect from the mongo database.
        """
        if self.__client is not None:
            self.__client.close()
            self.__logger.info("Database connection closed")

    def read_collection(self, collection_name: str, query: list[dict] = None):
        """
        Read a collection from the MongoDB database.
        """
        if query is None:
            query = []
        try:
            collection = self.__db[collection_name]
            data = list(collection.aggregate(query))
            self.__logger.info(f"Data loaded successfully from: {collection_name}")
            return data
        except Exception as e:
            self.__logger.error(f"Failed to retrieve collection : {e}")
            raise e
        
    def create_document(self, collection_name: str, data: dict | list[dict], many: bool = False):
        """
        Create a document and insert into the mongodb collection.
        """
        try:
            collection = self.__db[collection_name]
            result = collection.insert_one(data) if not many and isinstance(data, dict) else collection.insert_many(data)
            self.__logger.info(f"Data inserted successfully to: {collection_name}")
            return result.acknowledged
        except Exception as e:
            self.__logger.error(f"Failed to insert data: {e}")
            raise e

    