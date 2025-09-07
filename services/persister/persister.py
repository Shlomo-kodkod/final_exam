import uuid
from services.utils.utils import setup_logger

class Persister:
    def __init__(self):
        self.__logger = setup_logger("Persister")


    def create_file_uid(self, meta_data: dict, id_parm: list) -> str:
        "Create unique id based on metadata or with uuid"
        try:
            uid = "".join([meta_data[parm] for parm in id_parm])
            uid = uid.strip()
            self.__logger.info("Successfully created file id")
            return uid if len(uid) > 10 else str(uuid.uuid4())
        except Exception as e:
            self.__logger.error(f"Failed to create file id: {e}")
            return str(uuid.uuid4())
    
    
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

    

    

