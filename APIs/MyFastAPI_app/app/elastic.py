import os
from elasticsearch import Elasticsearch

def get_es_client():
    es_host = os.getenv("ES_HOST", "localhost:9200")  # Utilisation de localhost:9200 par défaut si la variable ES_HOST n'est pas définie
    return Elasticsearch(hosts=[f"http://{es_host}"])
