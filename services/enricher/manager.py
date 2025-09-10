from services.utils.logger import Logger
from services.utils.utils import base64_decoder
from services.kafka.consumer import KafkaConsumer
from services.enricher.enricher import Enricher
from services.dal.elastic import Elastic
from services import config


class EnricherManager:
    def __init__(self, threshold: float = 10.0):
        self.__logger = Logger.get_logger("EnricherManager")
        self.__threshold = threshold
        self.__enricher = Enricher()
        self.__elastic = Elastic(config.ES_URI)
        try: 
            topics = [config.KAFKA_ENRICHER_TOPIC]
            self.__consumer = KafkaConsumer(config.BOOTSTRAP_SERVER, config.KAFKA_ENRICHER_GROUP_ID, topics)
            self.__elastic.connect()
            self.__logger.info("EnricherManager successfully initialized")
        except Exception as e:
            self.__logger.error(f"Failed to initialize EnricherManager: {e}")

    def load_blacklist(self, encoded_blacklist: str) -> list:
        """
        Load and decode hostile words blacklist.
        """
        try:
            decoded_blacklist = base64_decoder(encoded_blacklist)
            blacklist = self.__enricher.split_text_to_word(decoded_blacklist)
            return blacklist
        except Exception as e:
            raise e
        

    def risk_calculation(self, text: str) -> float | None:
        """
        Calculates the percentage of hostility of the text.
        """
        try:
            total_words = len(text.split())
            hostile_blacklist = self.load_blacklist(config.HOSTILE_BLACKLIST)
            less_hostile_blacklist = self.load_blacklist(config.NOT_HOSTILE_BLACKLIST)
            hostile_score = self.__enricher.text_classification(text, hostile_blacklist) * 2
            not_hostile_score = self.__enricher.text_classification(text, less_hostile_blacklist)
            score = (hostile_score + not_hostile_score) / total_words * 100 if total_words > 0 else 0
            return score
        except Exception as e:
            raise Exception(f"Failed to calculate dangerous percentage: {e}")
        
    def is_risk(self, text: str) -> bool | None:
        """
        Check if risk percentage is over the threshold.
        """
        try: 
            score = self.risk_calculation(text)
            return score >= self.__threshold
        except Exception as e:
            raise e
        
    def risk_level(self, text: str) -> str | None:
        """
        Calculates the risk level.
        """
        try:
            score = self.risk_calculation(text)
            if score <= 5: return "None"
            elif score >= self.__threshold: return "High"
            else: return "Medium"
        except Exception as e:
            raise e
        
        
    def analyze_text(self, text):
        """
        Analyze text dangers level.
        """
        try:
            new_data = dict()
            new_data["Bad Percent"] = self.risk_calculation(text)
            new_data["Is Bad"] = self.is_risk(text)
            new_data["Bds Threat Level"] = self.risk_level(text)
            return new_data
        except Exception as e:
            raise e
        
    def get_text_by_id(self, file_id: str, text_label: str = "Text") -> str:
        """
        Return metadata text by id fom elastic.
        """
        try:
            document = self.__elastic.search(config.ES_INDEX, file_id)
            data = document[text_label]
            return data
        except Exception as e:
            self.__logger.error("")
            raise e


    def update_metadata(self, data: dict, field: str = "id"):
        """
        Update file metadata in elastic with new data. 
        """
        try:
            file_id = data[field]
            text = self.get_text_by_id(file_id)
            clean_text = self.__enricher.remove_punctuation(text)
            enricher_data = self.analyze_text(clean_text)
            self.__elastic.update_documents(config.ES_INDEX, file_id, enricher_data)
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



            
        
        
    
        




        

        
