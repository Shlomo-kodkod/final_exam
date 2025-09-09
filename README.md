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
- 


### phase 2:
- 


### phase 3:
- 


### phase 4:
- 


