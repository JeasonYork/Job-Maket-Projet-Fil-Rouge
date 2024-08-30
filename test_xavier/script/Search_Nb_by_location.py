from elasticsearch import Elasticsearch, helpers
import os
import json

es = Elasticsearch(
    hosts=["http://elastic:datascientest@localhost:9200"],
    # use_ssl=True,                # Indique que SSL est utilisé
    verify_certs=False,          # Désactive la vérification des certificats
    ssl_show_warn=False          # Désactive les avertissements de sécurité SSL
)

# Requête pour obtenir les modalités du champ "location" et le nombre de documents pour chaque modalité
search_query = {
    "size": 0,
    "aggs": {
        "location_terms": {
            "terms": {
                "field": "location.keyword",  # Utiliser le type keyword pour les agrégations
                "size": 1000  # Ajuster la taille selon le nombre attendu de modalités
            }
        }
    }
}

result = es.search(index="jobmarket", body=search_query)

# Extraction des résultats d'agrégation
location_buckets = result['aggregations']['location_terms']['buckets']
for bucket in location_buckets:
    location = bucket['key']
    doc_count = bucket['doc_count']
    print(f"Location: {location}, Nombre de documents: {doc_count}")
from elasticsearch import Elasticsearch, helpers
import os
import json

es = Elasticsearch(
    hosts=["http://elastic:datascientest@localhost:9200"],
    # use_ssl=True,                # Indique que SSL est utilisé
    verify_certs=False,          # Désactive la vérification des certificats
    ssl_show_warn=False          # Désactive les avertissements de sécurité SSL
)

# Requête pour obtenir les modalités du champ "location" et le nombre de documents pour chaque modalité
search_query = {
    "size": 0,
    "aggs": {
        "location_terms": {
            "terms": {
                "field": "location.keyword",  # Utiliser le type keyword pour les agrégations
                "size": 1000  # Ajuster la taille selon le nombre attendu de modalités
            }
        }
    }
}

result = es.search(index="jobmarket", body=search_query)

# Extraction des résultats d'agrégation
location_buckets = result['aggregations']['location_terms']['buckets']
for bucket in location_buckets:
    location = bucket['key']
    doc_count = bucket['doc_count']
    print(f"Location: {location}, Nombre de documents: {doc_count}")
