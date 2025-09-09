import hashlib
from services.utils.utils import Logger

class Persister:
    def __init__(self):
        self.__logger = Logger.get_logger("Persister")


    def create_file_uid(self, file_bytes: bytes) -> str:
        "Create unique id based on file data with hash"
        try:
            uid = hashlib.md5(file_bytes).hexdigest()
            self.__logger.info("Successfully create file unique id")
            return uid[:24]
        except Exception as e:
            self.__logger.error(f"Failed to create file id: {e}")
            raise
    
    
    def convert_audio_to_bin(self, file_path) -> bytes:
        """
        Convert audio file to binary.
        """
        try:
            with open(rf"{file_path}", "rb") as f:
                file_data = f.read()
            self.__logger.info(f"File {file_path} successfully converted")
            return file_data
        except Exception as e:
            self.__logger.error(f"Failed to convert file {file_path}: {e}")
            raise

    

    

