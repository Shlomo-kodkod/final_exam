from services.kafka.producer import KafkaProducer
from services.retriver.fetcher import Fetcher
from services.utils.utils import setup_logger
from services import config

class Manager:
    def __init__(self):
        self.__logger = setup_logger("Fetcher - Manager")
        self.__fetcher = Fetcher()
        self.__producer = KafkaProducer(config.BOOTSTRAP_SERVER)

    def publish_data(self, data: list[dict], topic: str, key: str):
        """
        Publish data to appropriate Kafka topics.
        """
        try:
            for record in data:
                self.__producer.produce(topic, key,  record)
                self.__logger.info(f"Published data to Kafka to topic {topic}")
        except Exception as e:
            self.__logger.error(f"Failed to publish data to topic {topic}: {e}")

    def main(self):
        data = self.__fetcher.create_file_records(config.DATA_PATH)
        self.publish_data(data, config.KAFKA_TOPIC, config.KAFKA_KEY)


