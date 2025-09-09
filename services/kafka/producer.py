import json
from confluent_kafka import Producer
from services.utils.utils import Logger


class KafkaProducer:
    def __init__(self, bootstrap_servers: str):
        self.__logger = Logger.get_logger("KafkaProducer")
        try:
            config = {'bootstrap.servers': bootstrap_servers}
            self.__producer = Producer(config)
            self.__logger.info(f"Kafka Producer created on {bootstrap_servers}")
        except Exception as e:
            self.__logger.error(f"Failed to create producer: {e}")
            raise 
    
    def delivery_report(self, error, message):
        """ 
        Check delivery status.
        """
        if error is not None:
            self.__logger.error(f"Message delivery failed: {error}")
        else:
            self.__logger.debug(f"Message delivered to {message.topic()}")

    def produce(self, topic: str, key: str, value: dict):
        """ 
        Send a message to Kafka topic
        """
        try:
            json_value = json.dumps(value).encode('utf-8')
            self.__producer.produce(topic, key=key.encode('utf-8') if key else None, value=json_value, callback=self.delivery_report)
            self.__producer.flush() 
            self.__logger.info(f"Produce message to topic {topic}")
        except Exception as e:
            self.__logger.error(f"Error on produce: {e}")
            raise

    def flush(self, timeout=10):
        """ 
        Wait for all messages in the Producer to be delivered 
        """
        self.__logger.info("Flushing producer")
        self.__producer.flush(timeout)
        self.__logger.info("Producer flush complete")

    def publish_data(self, data: list[dict], topic: str, key: str):
        """
        Publish data to appropriate Kafka topics.
        """
        try:
            for record in data:
                json_value = json.dumps(record).encode('utf-8')
                self.__producer.produce(topic, key=key.encode('utf-8') if key else None, value=json_value, callback=self.delivery_report)
                self.__logger.info(f"Published data to Kafka to topic {topic}")
                self.__producer.flush()
        except Exception as e:
            self.__logger.error(f"Failed to publish data to topic {topic}: {e}")

        