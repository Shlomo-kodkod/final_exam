import re
import string
from services.utils.logger import Logger




class Enricher:
    def __init__(self):
        self.__logger = Logger.get_logger("Enricher")

    def remove_punctuation(self, text: str) -> str:
        """
        Removes all punctuation marks from the text.
        """
        return text.translate(str.maketrans('', '', string.punctuation))


    def split_text_to_word(self, text: str, split_by: str = ",") -> list:
        """
        Split string to list of words.
        """
        return text.lower().split(sep=split_by)  
    
    def find_sum_all(self, word: str, text: str) -> int:
        """
        Returns the amount of instances of a word in a text.
        """
        expression = fr"\b{word}\b"
        match = re.findall(expression, text, flags=re.IGNORECASE)
        return len(match)


    def text_classification(self, text: str, blacklist: list):
        """
        Returns the content classification score by a given word list.
        """
        score = 0

        for word in blacklist:
            score += self.find_sum_all(word, text)
        self.__logger.info("Text classification has been successful")
        return score
        

