from services.dal.elastic import Elastic
from services.dal.mongo import Mongo
from services.kafka.consumer import KafkaConsumer
from services.utils.utils import Logger
from services.persister.persister import Persister
from services import config


class PersisterManager:
    def __init__(self):
        self.__logger = Logger.get_logger("PersisterManager")
        self.__elastic = Elastic(config.ES_URI)
        self.__mongo = Mongo(config.MONGO_URI)
        self.__persister = Persister()
        try: 
            topics = [config.KAFKA_TOPIC]
            self.__consumer = KafkaConsumer(config.BOOTSTRAP_SERVER, config.KAFKA_GROUP_ID, topics)
            self.__elastic.connect()
            self.__elastic.create_index(config.ES_INDEX, config.ES_MAPPING)
            self.__mongo.connect(config.MONGO_INITDB_DATABASE)
            self.__logger.info("PersisterManager successfully initialized")
        except Exception as e:
            self.__logger.error(f"Failed to initialize PersisterManager: {e}")

    
    def index_metadata(self, metadata, file_id: str):
        """
        Indexing file metadata in elastic.
        """
        try:
            metadata["File ID"] = file_id
            self.__elastic.index(config.ES_INDEX, metadata)

            self.__logger.info("Successfully index data to elastic")
        except Exception as e:
            self.__logger.error("Failed to index data to elastic")

    def process_message(self, message: dict, path_filed: str = "File Path"):
        """
        Process message, indexing in elastic and upload data to MongoDB.
        """
        try:
            file_data = self.__persister.convert_audio_to_bin(message[path_filed])  
            uid = self.__persister.create_file_uid(file_data)
            self.index_metadata(message, uid)
            self.__mongo.insert_file(uid, file_data)
            self.__logger.info(f"Successfully processed message with id: {uid}")
        except Exception as e:
            self.__logger.error(f"Failed to process message: {e}")

    def main(self):
        """
        Start consume and process messages from kafka.
        """
        try:
            self.__consumer.consume_messages(self.process_message)
        except Exception as e:
            self.__logger.error(f"Failed to consume messages: {e} ")
    






        


