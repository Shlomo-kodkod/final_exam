import json
from confluent_kafka import Consumer
from services.utils.utils import setup_logger


class KafkaConsumer:
    def __init__(self, bootstrap_servers: str, group_id: str, topics: list, auto_offset_reset='earliest'):
        self.__logger = setup_logger("KafkaConsumer")
        try:
            conf = {
                'bootstrap.servers': bootstrap_servers,
                'group.id': group_id,
                'auto.offset.reset': auto_offset_reset,
                'enable.auto.commit': True
            }
            self.consumer = Consumer(conf)
            self.consumer.subscribe(topics)
            self.__logger.info(f"Kafka Consumer initialized on topics {topics}, group_id {group_id}")
        except Exception as e:
            self.__logger.error(f"Failed to create consumer: {e}")
            raise
        self.__run = True
    

    def consume_messages(self, process_message):
        """
        Continuously consume messages and process them with the given callback.
        """
        self.__logger.info("Starting consumer")
        while self.__run:
            message = self.consumer.poll(1.0)

            if message is None:
                continue
            if message.error():
                self.__logger.error(f"Error: {message.error()}")
                continue

            try:
                value = json.loads(message.value().decode('utf-8')) if message.value() else None
                process_message(message.topic(), value)
                self.__logger.info(f"Received message from topic {message.topic()}")
            except Exception as e:
                self.__logger.error(f"Error while receiving message: {e}")
        
        self.consumer.close()
        self.__logger.info("Consumer closed")

    def stop(self):
        """
        Stop the consumer loop.
        """
        self.__run = False
        self.__logger.info("Consumer stopped")