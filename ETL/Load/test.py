from elasticsearch import Elasticsearch
import json

# Connectez-vous à Elasticsearch
es = Elasticsearch(
    hosts=["http://elastic:datascientest@localhost:9200"],
    verify_certs=False,
    ssl_show_warn=False
)

# Index Elasticsearch
index_name = 'jobmarket'

# Fonction pour obtenir toutes les valeurs uniques de la variable 'source' et leur nombre
def get_source_values_count(es, index_name):
    # Utilisez une agrégation de type 'terms' pour obtenir les valeurs uniques et leur nombre
    body = {
        "size": 0,
        "aggs": {
            "unique_sources": {
                "terms": {
                    "field": "source.keyword",
                    "size": 20000  # Limite le nombre de résultats retournés
                }
            } 
        }
    }
    
    response = es.search(index=index_name, body=body)
    source_buckets = response['aggregations']['unique_sources']['buckets']
    
    source_values = {bucket['key']: bucket['doc_count'] for bucket in source_buckets}
    
    return source_values

# Récupérez et imprimez les valeurs uniques de 'source' et leur nombre
source_values_count = get_source_values_count(es, index_name)
for source, count in source_values_count.items():
    print(f"Source: {source}, Count: {count}")

print("Les valeurs uniques de la variable 'source' et leur nombre ont été retournées.")
