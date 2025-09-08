import os

BOOTSTRAP_SERVER = os.getenv("BOOTSTRAP_SERVER", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "metadata")
KAFKA_KEY = os.getenv("KAFKA_KEY", "retriever")
KAFKA_GROUP_ID = os.getenv("KAFKA_GROUP_ID", "persister")
DATA_PATH = "podcasts"
ES_HOST = os.getenv("ES_HOST", "localhost")
ES_PORT = os.getenv("ES_PORT", 9200)
ES_INDEX = os.getenv("ES_INDEX", "podcast_metadata")
MONGO_PROTOCOL = os.getenv("MONGO_PROTOCOL", "mongodb")
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT=int(os.getenv("MONGO_PORT", 27017))
MONGO_INITDB_DATABASE = os.getenv("MONGO_INITDB_DATABASE", "podcast")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "podcast")
MONGO_URI = f"{MONGO_PROTOCOL}://{MONGO_HOST}:{MONGO_PORT}/"
ES_URI = f"http://{ES_HOST}:{ES_PORT}"

ES_MAPPING = {
    "properties": {
        "File Path": {"type": "keyword"},
        "File Name": {"type": "keyword"},
        "Size (KB)": {"type": "float"},
        "Creation Date": {
            "type": "date",
            "format": "yyyyMMdd'T'HHmmssZ"
            },
        "Modified Date": {
            "type": "date",
            "format": "yyyyMMdd'T'HHmmssZ"
            },
        "Last Access Date": {
            "type": "date",
            "format": "yyyyMMdd'T'HHmmssZ"
        }
    }
}