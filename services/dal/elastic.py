from elasticsearch import Elasticsearch , helpers
from services.utils.utils import setup_logger


class Elastic:
    def __init__(self, uri):
        self.__uri = uri
        self.__connection = None 
        self.__logger = setup_logger("Elastic")

    def connect(self):
        """
        Connect to elasticsearch server.
        """
        try:
<<<<<<< HEAD
            self.__connection = Elasticsearch([self.__uri])
=======
            self.__connection = Elasticsearch([self.__uri], verify_certs=True)
>>>>>>> f79dfeb937f234e1f45b6a0155e92848ad7f61f6
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
            
        
    def index(self, index_name: str, data: list[dict]):
        """
        Indexing documents into elasticsearch.
        """
        try:
            actions = [{"_index": index_name, "_source": doc} for doc in data]
            helpers.bulk(client=self.__connection, actions=actions)
            self.__logger.info(f"Successfully indexed {len(actions)} documents in {index_name}")
        except Exception as e:
            self.__logger.error(f"Failed to index data in {index_name}: {e}")
            raise e
        
        
    def search(self, index_name: str, query: dict = {"query": {"match_all": {}}}, score: bool = False) -> list:
        """
        Searches for documents in elasticsearch index.
        """
        try:
            result = helpers.scan(client=self.__connection, index=index_name, query=query)
            docs = [document["_source"] for document in result] if score else [document for document in result]
            self.__logger.info(f"Successfully search in {index_name}")
            return docs 
        except Exception as e:
            self.__logger.error(f"Failed to search in {index_name}: {e}")
            raise e
            
                         


    