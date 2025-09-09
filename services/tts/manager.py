from services.utils.utils import Logger
from services.tts.tts import Tts
from services.dal.elastic import Elastic
from services.dal.mongo import Mongo
from services import config

class TtsManager:
    def __init__(self):
        self.__logger = Logger.get_logger("TtsManager")
        self.__transcriber = Tts()
        self.__elastic = Elastic(config.ES_URI)
        self.__mongo = Mongo(config.MONGO_URI)
        try: 
            self.__elastic.connect()
            self.__mongo.connect(config.MONGO_INITDB_DATABASE)
            self.__logger.info("TtsManager successfully initialized")
        except Exception as e:
            self.__logger.error(f"Failed to initialize TtsManager: {e}")

    def load_elastic_ids(self, index_name: str, id_label: str = 'File ID') -> list:
        try:
            result = self.__elastic.search(index_name)
            ids = [doc.get(id_label, "") for doc in result]
            self.__logger.info(f"Successfully load elastic data from {index_name}")
            return ids
        except Exception as e:
            self.__logger.error(f"Failed to load elastic data from {index_name}: {e}")
            raise e
        
    
        
a = TtsManager()
f = a.load_elastic_ids(config.ES_INDEX)
print(f)
        
    

    

    

    