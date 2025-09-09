import os

BOOTSTRAP_SERVER = os.getenv("BOOTSTRAP_SERVER", "localhost:9092")

KAFKA_META_TOPIC = os.getenv("KAFKA_META_TOPIC", "metadata")
KAFKA_AUDIO_TOPIC = os.getenv("KAFKA_AUDIO_TOPIC", "audio")
KAFKA_META_KEY = os.getenv("KAFKA_META_KEY", "metaretriever")
KAFKA_META_GROUP_ID = os.getenv("KAFKA_META_GROUP_ID", "metapersister")
KAFKA_AUDIO_KEY = os.getenv("KAFKA_META_KEY", "audioretriever")
KAFKA_AUDIO_GROUP_ID = os.getenv("KAFKA_META_GROUP_ID", "audiopersister")


DATA_PATH = "podcasts"

ES_HOST = os.getenv("ES_HOST", "localhost")
ES_PORT = os.getenv("ES_PORT", 9200)
ES_INDEX = os.getenv("ES_INDEX", "podcast_metadata")
ES_LOG_INDEX = os.getenv("ES_LOG_INDEX", "logger")
ES_URI = f"http://{ES_HOST}:{ES_PORT}"


MONGO_PROTOCOL = os.getenv("MONGO_PROTOCOL", "mongodb")
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = os.getenv("MONGO_PORT", 27017)
MONGO_INITDB_DATABASE = os.getenv("MONGO_INITDB_DATABASE", "podcast")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "podcast")
MONGO_URI = f"{MONGO_PROTOCOL}://{MONGO_HOST}:{MONGO_PORT}/"

ES_MAPPING = {
    "properties": {
        "File ID" : {"type": "keyword"},
        "File Path": {"type": "keyword"},
        'Suffix': {"type": "keyword"},
        "File Name": {"type": "keyword"},
        "Size (KB)": {"type": "float"},
        "Creation Date": {
            "type": "date",
            "format": "yyyy-MM-dd"
                          },
        "Modified Date": {
            "type": "date",
             "format": "yyyy-MM-dd"
            },
        "Last Access Date": {
            "type": "date",
             "format": "yyyy-MM-dd"
            },
        "Text" : {"type": "text"}
    }
}