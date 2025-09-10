from elasticsearch import Elasticsearch , helpers
from services.utils.logger import Logger
from services import config

class Elastic:
    def __init__(self, uri):
        self.__uri = uri
        self.__connection = None 
        self.__logger = Logger.get_logger("Elastic")

    def connect(self):
        """
        Connect to elasticsearch server.
        """
        try:
            self.__connection = Elasticsearch([self.__uri], verify_certs=True)
            if self.__connection.ping():
                self.__logger.info("Successfully connected to Elasticsearch")
            else:
                self.__logger.error("Failed to connect to Elasticsearch")
        except Exception as e:
            self.__logger.error(f"Failed to connect to elastic {e}")
            raise e

    def create_index(self, index_name: str, mappings: dict):
        """
        Creates a new index in elasticsearch if it doesn't exist.
        """
        if not self.__connection.indices.exists(index=index_name):
            self.__connection.indices.create(index=index_name, mappings=mappings)
            self.__logger.info(f"Successfully create index {index_name}")
        else:
            self.__logger.warning(f"Index {index_name} already exists")
            
        
    def index(self, index_name: str, file_id: str, data: dict):
        """
        Indexing documents into elasticsearch.
        """
        try:
            self.__connection.index(index=index_name, id=file_id, document=data)
            self.__logger.info(f"Successfully indexed document in {index_name} with id: {file_id}")
        except Exception as e:
            self.__logger.error(f"Failed to index data in {index_name}: {e}")
            raise e
        
        
    def search(self, index_name: str, file_id: str) -> list:
        """
        Searches for documents in elasticsearch index.
        """
        try:
            result = self.__connection.get(index=index_name, id=file_id)
            if result['found']:
                doc = result['_source']
                self.__logger.info(f"Document with ID: {file_id} found in index: {index_name}")
                return doc 
            else:
                self.__logger.info(f"Document with ID: {file_id} not found in index: {index_name}")
                raise Exception(f"Document with ID: {file_id} not found in index: {index_name}")
        except Exception as e:
            self.__logger.error(f"Failed to search in {index_name}: {e}")
            raise e
        

    def update_documents(self, index_name: str, id:str, data: dict):
        """
        Updates existing document in elasticsearch.
        """
        try:
            self.__connection.update(index=index_name, id=id, doc=data)
            self.__logger.info(f"Successfully update document {id}")
        except Exception as e:
            self.__logger.error(f"Failed to update document {id}: {e}")
            raise e
   