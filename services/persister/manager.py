from services.dal.elastic import Elastic
from services.dal.mongo import Mongo
from services.utils.utils import setup_logger
from services.persister.persister import Persister
from services import config


class Manager:
    def __init__(self):
        self.__logger = setup_logger("Persister - Manager")
        self.__elastic = Elastic(config.ES_URI)
        self.__elastic.connect()
        self.__elastic.create_index(config.ES_INDEX, config.ES_MAPPING)
        self.__mongo = Mongo(config.MONGO_URI)
        self.__mongo.connect(config.MONGO_INITDB_DATABASE)

    def upload_data_dict(self, file_id: str, file_data: bytes):
        """
        Upload the data to mongodb.
        """
        try:
            data =   {
                        "file_id": file_id,
                        "file_data": file_data
                            }
            self.__mongo.create_document(config.MONGO_COLLECTION, data)
            self.__logger.info(f"Successful insert file data to dict")
        except Exception as e:
            self.__logger.error("")
        
    
    def index_metadata(self, metadata, file_id: str):
        try:
            metadata["file_id"] = file_id
            data = [metadata]
            self.__elastic.index(config.ES_INDEX, data)
            self.__logger.info("Successfully index data to elastic")
        except Exception as e:
            self.__logger.info("Failed to index data to elastic")

   
        







        



