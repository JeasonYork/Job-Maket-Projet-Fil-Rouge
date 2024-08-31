import json
import os
from collections import Counter

input_directory = "/home/ubuntu/test_mohamed/bases"

for filename in os.listdir(input_directory):
    if filename.endswith("_updated.json"):
        json_file = os.path.join(input_directory, filename)

        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        job_title_bis_values = [entry['job_title_bis'] for entry in data]
        counter = Counter(job_title_bis_values)

        # Afficher les différentes valeurs de job_title_bis ainsi que leur nombre
        #print(f"Résumé pour le fichier : {filename}")
        #for job_title, count in counter.items():
        #    print(f"{job_title}: {count}")

        import pandas as pd
        df = pd.DataFrame(counter.items(), columns=['job_title_bis', 'count'])
        print(df)


"""for entry in data:
    if entry['job_title_bis'] == "Other":
        print(entry.get('title', 'Titre inconnu'))"""
