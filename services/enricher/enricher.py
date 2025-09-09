from services.utils.logger import Logger




class Enricher:
    def __init__(self):
        self.__logger = Logger.get_logger("Enricher")


    def split_text_to_word(self, text: str, split_by: str = " ") -> list:
        """
        Split string to list of words.
        """
        return text.lower().split()  


    def analyze_sentiment(self, text: str, hostile_blacklist: list, not_hostile_blacklist: list):
        """
        """
        sentiment_score = 0
        found_words = 0

        for word in text:
            if word in hostile_blacklist:
                sentiment_score += 2
                found_words += 1
            if word in not_hostile_blacklist:
                sentiment_score += 1
                found_words += 1

        if found_words > 0:
            return sentiment_score / found_words  
        else:
            return 0  