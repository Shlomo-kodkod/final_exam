from services.utils.logger import Logger
from services.tts.tts import Tts
from services.dal.elastic import Elastic
from services.dal.mongo import Mongo
from services.kafka.consumer import KafkaConsumer
from services import config

class TtsManager:
    def __init__(self):
        self.__logger = Logger.get_logger("TtsManager")
        self.__transcriber = Tts()
        self.__elastic = Elastic(config.ES_URI)
        self.__mongo = Mongo(config.MONGO_URI)
        try: 
            topics = [config.KAFKA_AUDIO_TOPIC]
            self.__consumer = KafkaConsumer(config.BOOTSTRAP_SERVER, config.KAFKA_AUDIO_GROUP_ID, topics)
            self.__elastic.connect()
            self.__mongo.connect(config.MONGO_INITDB_DATABASE)
            self.__logger.info("TtsManager successfully initialized")
        except Exception as e:
            self.__logger.error(f"Failed to initialize TtsManager: {e}")

        
    def transcribe_by_id(self, file_id:str):
        """
        Retrieve audio data from mongo by id and transcribe the audio. 
        """
        try:
            audio_file = self.__mongo.find_file(file_id)
            audio_data = audio_file.read()
            result = self.__transcriber.transcribe(audio_data)
            self.__logger.info(f"Successfully transcribe audio data with id {file_id}")
            return result
        except Exception as e:
            self.__logger.error(f"Failed to transcribe audio data with id {file_id}: {e}")
            raise e

    def update_metadata(self, data: dict, filed: str = "id"):
        """
        Update file metadata in elastic with audio data. 
        """
        try:
            
            id = data[filed]
            text = self.transcribe_by_id(id)
            data = {"Text": text}
            self.__elastic.update_documents(config.ES_INDEX, id, data)
            self.__logger.info(f"Successfully update metadata in file id {id}")
        except Exception as e:
            self.__logger.error(f"Failed to update metadata in file id {id}: {e}")
            raise e



    def main(self):
        """
        Start transcribe files data and update metadata in elastic.
        """
        try:
            self.__consumer.consume_messages(self.update_metadata)
        except Exception as e:
            self.__logger.error(f"Failed to consume messages: {e} ")
        
  
