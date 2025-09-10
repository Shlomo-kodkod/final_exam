import re
from services.utils.logger import Logger




class Enricher:
    def __init__(self):
        self.__logger = Logger.get_logger("Enricher")


    def split_text_to_word(self, text: str, split_by: str = ",") -> list:
        """
        Split string to list of words.
        """
        return text.lower().split()  
    
    def find_sum_all(self, word: str, text: str) -> int:
        """
        Returns the amount of instances of a word in a text.
        """
        expression = fr"\b{word}\b"
        match = re.findall(expression, text, flags=re.IGNORECASE)
        return len(match)


    def text_classification(self, text: str, blacklist: list):
        """
        Returns the content classification percentage by a given word list.
        """
        total_words = len(text.split())
        score = 0

        for word in blacklist:
            score += self.find_sum_all(word, text)
        result = (score / total_words) * 100 if total_words > 0 else 0
        return result
        


