from elasticsearch import Elasticsearch

# Connexion à Elasticsearch
es = Elasticsearch(
    hosts=["http://elastic:datascientest@localhost:9200"],
    verify_certs=False,
    ssl_show_warn=False
)

# Définir les modifications à apporter
modifications = [
    {
        "old_key": "Data Analytics",
        "new_key": "DataAnalytics"
    },
    {
        "old_key": "MachingLearning",
        "new_key": "MachineLearning"
    },
    {
        "old_key": "OS",
        "new_key": "Os"
    }
]

# Parcourir les modifications et exécuter les requêtes de mise à jour
for modification in modifications:
    query = {
        "script": {
            "source": f"""
                if (ctx._source.skills.containsKey('{modification['old_key']}')) {{
                    def value = ctx._source.skills.remove('{modification['old_key']}');
                    ctx._source.skills['{modification['new_key']}'] = value;
                }}
            """,
            "lang": "painless"
        }
    }

    # Exécuter la requête de mise à jour par requête
    es.update_by_query(index='jobmarket', body=query)
