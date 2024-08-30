from elasticsearch import Elasticsearch, NotFoundError

# Connexion à Elasticsearch
es = Elasticsearch(
        hosts=["http://elastic:datascientest@localhost:9200"],
        verify_certs=False,
        ssl_show_warn=False
    )

# Définir l'index à utiliser
index_name = "jobmarket"

def delete_duplicates():
    # Requête pour trouver les doublons
    query = {
        "size": 0,
        "query": {
            "term": {
                "source.keyword": "France Travail"
            }
        },
        "aggs": {
            "duplicate_links": {
                "terms": {
                    "field": "link.keyword",
                    "min_doc_count": 2
                },
                "aggs": {
                    "duplicate_docs": {
                        "top_hits": {
                            "size": 10,
                            "_source": {
                                "includes": ["link"]
                            }
                        }
                    }
                }
            }
        }
    }

    # Exécuter la requête pour trouver les doublons
    response = es.search(index=index_name, body=query)

    # Vérifier si des doublons existent
    duplicate_buckets = response['aggregations']['duplicate_links']['buckets']
    if not duplicate_buckets:
        return False

    # Parcourir les doublons et les supprimer
    for bucket in duplicate_buckets:
        docs = bucket['duplicate_docs']['hits']['hits']

        # Conserver le premier document et supprimer les autres
        for doc in docs[1:]:  # On commence à partir de 1 pour éviter de supprimer le premier document
            doc_id = doc['_id']
            try:
                es.delete(index=index_name, id=doc_id)
                print(f"Document {doc_id} supprimé.")
            except NotFoundError:
                print(f"Document {doc_id} n'a pas été trouvé, probablement déjà supprimé.")

    return True

# Boucle pour supprimer les doublons jusqu'à ce qu'il n'en reste plus
while delete_duplicates():
    print("Un autre lot de doublons supprimé, recherche de plus de doublons...")

print("Tous les doublons ont été supprimés.")
