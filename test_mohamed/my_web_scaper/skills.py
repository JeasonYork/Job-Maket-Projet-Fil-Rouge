from pathlib import Path
import json
import re
import datetime

# Votre dictionnaire de compétences
skills = {
    "ProgLanguage": [
        "Python",
        "Java",
        "C++",
        "C#",
        "Scala",
        "R",
        "Julia",
        "Kotlin",
        "Bash",
    ],
    "DataBase": [
        "SQL",
        "NoSQL",
        "MongoDB",
        "Cassandra",
        "Neo4j",
        "HBase",
        "Elasticsearch",
    ],
    "DataAnalytics": [
        "Pandas",
        "NumPy",
        "R",
        "MATLAB",
    ],
    "BigData": [
        "Hadoop",
        "Spark",
        "Databricks",
        "Flink",
        "Apache Airflow",
    ],
    "MachineLearning": [
        "Scikit-Learn",
        "TensorFlow",
        "Keras",
        "PyTorch",
        "XGBoost",
        "LightGBM",
        "CatBoost",
        "Orange",
    ],
    "DataSerialization": [
        "Avro",
        "Protocol Buffers",
        "Json",
        "XML",
    ],
    "DataVisualisation": [
        "Tableau",
        "Power BI",
        "Matplotlib",
        "Seaborn",
        "Plotly",
    ],
    "Statistics": [
        "Statistiques Descriptives",
        "Inférentielles",
        "Bayesian Statistics",
        "Statistiques Bayésiennes",
    ],
    "CloudComputing": [
        "AWS",
        "Azure",
        "Google Cloud Platform",
        "GCP",
        "IBM Cloud",
        "Alibaba Cloud",
    ],
    "DevTools": ["Git", "Docker", "Jenkins", "Travis CI"],
    "OS": ["Linux", "Windows", "MacOS"],
    "DBMS": [
        "MySQL",
        "PostgreSQL",
        "Oracle SQL",
        "SQL Server",
        "Snowflake",
        "BigQuery",
        "Big Query",
        "SingleStore",
    ],
    "SoftBigDataProcessing": ["Apache Kafka", "Apache Flink", "HBase", "Cassandra"],
    "Automation": [
        "Ansible",
        "Kubernetes",
        "Puppet",
        "Chef",
        "Airflow",
    ],
    "InfrastructureAsCode": ["Terraform", "CloudFormation"],
    "NetworkSecurty": ["VPN", "Firewall", "SSL/TLS", "Wireshark"],
    "Virtualisation": ["VMware", "VirtualBox", "Hyper-V"],
    "Containers": ["Docker", "Kubernetes", "OpenShift"],
    "Collaboration": [
        "JIRA",
        "Confluence",
        "Slack",
        "Microsoft Teams",
        "Teams",
        "Discord",
    ],
    "Other": [
        "DevOps",
        "Backend Development",
        "Big Data",
        "ML",
        "Machine Learning",
        "Statistiques",
        "Cloud",
        "CI/CD",
        "CI / CD",
    ],
    "EnSoftSkils": [
        "Communication",
        "Teamwork",
        "Time Management",
        "Adaptability",
        "Problem Solving",
        "Leadership",
        "Creativity",
        "Empathy",
        "Collaboration",
        "Stress Management",
        "Organization",
        "Flexibility",
        "Initiative",
        "Critical Thinking",
        "Interpersonal Skills",
    ],
}


# Fonction pour vérifier la présence de mots en entier et insensible à la casse
def find_skills(description, skills):
    found_skills = {}
    description = description.lower()
    for category, keywords in skills.items():
        found_keywords = set()  # Utiliser un set pour supprimer les doublons
        for keyword in keywords:
            # Utilisation de regex pour trouver des mots complets, insensible à la casse
            pattern = re.compile(r"\b" + re.escape(keyword.lower().strip()) + r"\b")
            if pattern.search(description):
                found_keywords.add(keyword)
        if found_keywords:
            found_skills[category] = list(found_keywords)  # Convertir le set en liste
    return found_skills


# Chemin vers le fichier JSON existant
data_dir = Path(__file__).resolve().parent / "data"
week_number = datetime.datetime.now().isocalendar()[1]
file_path = data_dir / f"wttj_database_{week_number}.json"

# Charger le fichier JSON
with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Parcourir les descriptions et trouver les compétences
for item in data:
    if "description" in item:
        item_description = item["description"]
        skills_found = find_skills(item_description, skills)
        item["skills"] = skills_found  # Ajouter les compétences trouvées à l'élément

# Écraser les données enrichies dans le fichier JSON existant
with open(file_path, "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print(f"Les données enrichies ont été enregistrées dans {file_path}")
