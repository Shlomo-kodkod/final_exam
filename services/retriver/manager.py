from services.kafka.producer import KafkaProducer
from services.retriver.fetcher import Fetcher
from services.utils.utils import Logger
from services import config

class FetcherManager:
    def __init__(self):
        self.__logger = Logger.get_logger("FetcherManager")
        self.__fetcher = Fetcher()
        try:
            self.__producer = KafkaProducer(config.BOOTSTRAP_SERVER)
            self.__logger.info("FetcherManager successfully initialized")
        except Exception as e:
            self.__logger.error("Failed to initialize FetcherManager")

    def main(self):
        """
        Start extracting files metadata and publish them to kafka.
        """
        data = self.__fetcher.create_file_records(config.DATA_PATH)
        self.__producer.publish_data(data, config.KAFKA_META_TOPIC, config.KAFKA_META_KEY)



