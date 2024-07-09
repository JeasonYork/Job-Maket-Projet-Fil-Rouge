from elasticsearch import Elasticsearch, helpers
import os
import json

es = Elasticsearch(
    hosts=["http://elastic:datascientest@localhost:9200"],
    #use_ssl=True,                # Indique que SSL est utilisé
    verify_certs=False,          # Désactive la vérification des certificats
    ssl_show_warn=False          # Désactive les avertissements de sécurité SSL
)

result = es.search(index="jobmarket", size=10000)  # Récupère les premiers 10000 documents, vous pouvez ajuster la taille selon vos besoins
ids = [doc['_id'] for doc in result['hits']['hits']]
print("Liste des IDs de documents dans l'index 'jobmarket':", ids[0])

search_query = {
    "size": 0,
    "aggs": {
        "top_prog_languages": {
            "terms": {
                "field": "ProgLanguage",
                "size": 1000  # Limite le nombre de valeurs retournées à 10
            }
        }
    }
}

result = es.search(index="jobmarket", body=search_query)

result = es.search(index="jobmarket", size=20)

for hit in result['hits']['hits']:
    doc_id = hit['_id']
    skills = hit['_source'].get('skills', {})
    prog_languages = skills.get('ProgLanguage', [])
    print(f"Document ID: {doc_id}, ProgLanguage: {prog_languages}")