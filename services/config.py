import os

BOOTSTRAP_SERVER = os.getenv("KAFKA_TOPIC", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "metadata")
KAFKA_KEY = os.getenv("KAFKA_TOPIC", "retriever")
DATA_PATH = "podcasts"

