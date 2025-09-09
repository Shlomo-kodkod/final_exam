from services.utils.utils import Logger
from services.tts.tts import Tts
from services.dal.elastic import Elastic
from services.dal.mongo import Mongo
from services.kafka.producer import KafkaProducer
from services import config

class TtsManager:
    def __init__(self):
        self.__logger = Logger.get_logger("TtsManager")
        self.__transcriber = Tts()
        self.__elastic = Elastic(config.ES_URI)
        self.__mongo = Mongo(config.MONGO_URI)
        self.__producer = KafkaProducer(config.BOOTSTRAP_SERVER)
        try: 
            self.__elastic.connect()
            self.__mongo.connect(config.MONGO_INITDB_DATABASE)
            self.__logger.info("TtsManager successfully initialized")
        except Exception as e:
            self.__logger.error(f"Failed to initialize TtsManager: {e}")

    def load_elastic_ids(self, index_name: str, id_label: str = 'File ID') -> list:
        """
        """
        try:
            result = self.__elastic.search(index_name)
            ids = [doc.get(id_label, "") for doc in result]
            self.__logger.info(f"Successfully load elastic data from {index_name}")
            return ids
        except Exception as e:
            self.__logger.error(f"Failed to load elastic data from {index_name}: {e}")
            raise e
        
    def retrieve_audio(self, file_id:str):
        """
        """
        try:
            audio_file = self.__mongo.find_file(file_id)
            self.__logger.info(f"Successfully load audio data with id {file_id}")
            audio_data = audio_file.read()
            return audio_data
        except Exception as e:
            self.__logger.error(f"Failed to load load audio data with id {file_id}: {e}")
            raise e


    def main(self):
        """
        Start transcribe files data and publish them to kafka.
        """
        ids = self.load_elastic_ids(config.ES_INDEX)
        for id in ids:
            try:
                audio_bytes = self.retrieve_audio(id)
                data = {"ID": id, "Audio": self.__transcriber.transcribe(audio_bytes)}
                self.__producer.produce(topic=config.KAFKA_AUDIO_TOPIC, key=config.KAFKA_AUDIO_KEY, value=data)
                self.__producer.flush()
                self.__logger.info(f"Successfully publish audio data with id {id}")
            except Exception as e:
                self.__logger.error(f"Failed to publish audio data with id {id}: {e}")
                continue




