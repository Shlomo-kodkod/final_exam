import os

BOOTSTRAP_SERVER = os.getenv("KAFKA_TOPIC", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "metadata")
KAFKA_KEY = os.getenv("KAFKA_TOPIC", "retriever")
KAFKA_GROUP_ID = os.getenv("KAFKA_GROUP_ID", "persister")
DATA_PATH = "podcasts"
ES_HOST = os.getenv("ES_HOST", "localhost")
ES_PORT = os.getenv("ES_PORT", 9200)
ES_INDEX = os.getenv("ES_INDEX", "podcast_metadata")

