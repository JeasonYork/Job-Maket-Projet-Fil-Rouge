import json
from pathlib import Path

current_path = Path(__file__).resolve().parent
doc_path = Path.joinpath(current_path, "old_databases", "indeed_final_db_bronze_v4.json")

# Initialiser une liste pour stocker chaque objet JSON
data = []

# Charger le fichier JSON ligne par ligne
with open(doc_path, 'r', encoding='utf-8') as f:
    for line in f:
        # Charger l'objet JSON de la ligne courante
        obj = json.loads(line)

        # Créer une nouvelle structure de dictionnaire avec les variables renommées
        new_obj = {
            "source": "Indeed",
            "company_data": {
                "sector": obj.get("company_industry"),
                "company_size": obj.get("company_size"),
                "turnover_in_millions": obj.get("company_turnover")
            },
            "skills": {
                "ProgLanguage": obj.get("Langages de Programmation"),
                "DataBase": obj.get("Bases de Données"),
                "Data Analytics": obj.get("Analyse de Données"),
                "BigData": obj.get("Big Data"),
                "MachineLearning": obj.get("Machine Learning et Data Mining"),
                "DataVisualisation": obj.get("Visualisation de Données"),
                "Statistics": obj.get("Statistiques"),
                "CloudComputing": obj.get("Cloud Computing"),
                "DevTools": obj.get("Outils de Développement"),
                "OS": obj.get("Systèmes d'Exploitation"),
                "SoftBigDataProcessing": obj.get("Big Data et Processing"),
                "Automation": obj.get("Automatisation et Orchestration"),
                "InfrastructureAsCode": obj.get("Infrastructure as Code (IaC)"),
                "NetworkSecurty": obj.get("Sécurité et Réseau"),
                "Virtualisation": obj.get("Virtualisation"),
                "Containers": obj.get("Containers"),
                "Collaboration": obj.get("Outils de Collaboration"),
                "Other": obj.get("Compétences")
            },
            "contract_type": obj.get("contract_type"),
            "salary": obj.get("salary"),
            "company": obj.get("company"),
            "location": obj.get("job_location"),
            "remote": obj.get("remote"),
            "title": obj.get("job_title"),
            "description": obj.get("raw_description")
        }

        # Ajouter le nouveau dictionnaire à la liste
        data.append(new_obj)

output_doc = Path.joinpath(current_path, "data", "indeed_gold.json")
# Sauvegarder les modifications dans un nouveau fichier JSON
with open(output_doc, 'w', encoding='utf-8') as f:
    # Écrire la liste de dictionnaires dans le fichier JSON
    json.dump(data, f, ensure_ascii=False, indent=4)
