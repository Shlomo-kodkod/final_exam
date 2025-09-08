from pymongo import MongoClient
import gridfs
from services.utils.utils import Logger

class Mongo:
    def __init__(self, uri):
        self.__logger = Logger.get_logger("Mongo")
        self.__uri = uri
        self.__client = None
        self.__db = None
        self.__fs = None

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
            self.__fs = gridfs.GridFS(self.__db)
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


    def insert_file(self, file_id: str, file_data: bytes):
        """
        Insert a file into the mongodb with id.
        """
        try: 
            id = self.__fs.put(data=file_data, files_id= file_id)
            self.__logger.info(f"File inserted successfully with file_id: {file_id}")
        except Exception as e:
            self.__logger.error(f"Failed to insert file {id}: {file_id}")
            raise

    def find_file(self, file_id: str) -> bytes | None:
        """
        Read a file from the MongoDB database based on file id.
        """
        try:
            file_data = self.__fs.find_one({'files_id': file_id})
            if file_data:
                self.__logger.info(f"Successfully load file {file_id}")
            else:
                self.__logger.info(f"File id {file_id} not found")
            return file_data
        except Exception as e:
            self.__logger.error(f"Failed to retrieve file {file_id}: {e}")
            raise

    def delete_file(self, file_id: str):
        """
        Delete a file from the MongoDB database based on file id.
        """
        try:
            self.__fs.delete(file_id)
            self.__logger.info(f"File with file_id: {file_id} has been deleted")
        except Exception as e:
            self.__logger.error(f"Failed to delete file with file_id {file_id} : {e}")
            raise


    


    