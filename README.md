# Muezzin -   المؤذن Project

## Text to speech pipeline microservices with Apache Kafka, MongoDB, elasticSearch.

### Retriever Service
- load audio path from audio files and post them to Kafka
- extract audio metadata and post them to kafka

### Persister Service  
- create unique id 
- convert audio content to bytes and save it in mongo
- save the metadata in elastic

### Tts Service
- transcribe audio content and add it to metadata in elastic

### Enricher Service
- risk analysis
- set a threshold for danger
- rating the danger levels


## Project structure

```
├──podcast/       # audio data
├──services/
|  ├── dal/             # Mongo and elastic dal
|  ├── enricher/        # Data enrichment service
|  ├── kafka/           # Kafka service
|  ├── persister/       # Data saving service
|  ├── retriever/       # Data retrieval service
|  ├── tts/             # Text to speech service
|  └── utiles/
└──README.md
```



## Explanations:

### phase 1:
- This service class loads audio files from local storage and extracts the metadata from the file using pathlib and os and sends it to the appropriate subject in Kafka.


### phase 2:
- The Persister service creates a unique identifier file with a hash that matches the ID in Mongo and converts the files to bytes and stores them in Mongo using gridfs to match large files.
- The service indexes the metadata in Elastic and stores the metadata for each file.


### phase 3:
- Tts transcripts each audio file separately using a conversion to BytesIOs and a faster_Whisper for fast performance without a heavy model.

#### Audio transcription service:
- I chose to develop a service dedicated to transcription so as not to create a load on the audio retention service and to transcribe only after receiving an update that the audio was uploaded.

### phase 4:
- The enricher service analyzes the text's danger with a list of dangerous words and finds text with the help of the re library for finding words.
- The service updates the new information in the existing metadata in Elastic.

#### Percentage of risk:
- I chose to calculates the percentage of risk according to the appearance number of each word from the list in text with a double ratio to a hostile word parts of the text basket in order to maintain a correct ratio.

#### Set a threshold for a dangerous event:
- I chose to set a threshold for a dangerous event by default at 10 percent to receive only dangerous alerts.

#### Rating the danger level:
- Rating the level of danger as high when it is equal or above the threshold of the dangerous event.
- The level of danger is not dangerous when it is below 5%, as this is not a real threat.
- The risk rating is moderate when it is between the low and the dangerous threshold to check if there is a threat.


