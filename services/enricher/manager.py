from services.utils.logger import Logger
from services.utils.utils import base64_decoder
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
            hostile_blacklist = self.load_blacklist(config.HOSTILE_BLACKLIST)
            less_hostile_blacklist = self.load_blacklist(config.NOT_HOSTILE_BLACKLIST)

            hostile_score = self.__enricher.text_classification(text, hostile_blacklist) * 2
            not_hostile_score = self.__enricher.text_classification(text, less_hostile_blacklist)
            score = hostile_score + not_hostile_score
            self.__logger.info("Successfully calculated dangerous percentage")
            return score
        except Exception as e:
            self.__logger.error(f"Failed to calculate dangerous percentage: {e}")
            return None
        




        

        
