import datetime
import json
import os
import re
from pathlib import Path

# Obtenir la date actuelle sous forme de chaîne formatée
current_date = datetime.datetime.now().strftime("%Y-%m-%d")

# Définir les répertoires
data_dir = Path('/opt/airflow/ETL/Json_scraping')
output_dir = Path('/opt/airflow/ETL/Json_transformed')

# Construire le nom de fichier final avec la date
final_file = f"wttj_database_{current_date}_updated.json"
output_filepath = output_dir / final_file

# Dictionnaire des métiers
JOBS = {
    "data engineer": (("data", "engineer"), ("data", "ingénieur")),
    "data architect": (("data", "architect"), ("architect", "si"), ("architect", "it")),
    "data scientist": (("data", "scientist"), ("science", "donnée")),
    "data analyst": (("data", "analyst"), ("data", "analytics")),
    "software engineer": (
        ("software", "engineer"),
        ("software", "developer"),
        ("développeur", "logiciel"),
        ("ingénieur", "logiciel"),
    ),
    "devops": ("devops",),
    "data warehousing engineer": ("data", "warehouse", "engineer"),
    "machine learning engineer": (
        ("machine", "learning", "engineer"),
        ("ml", "engineer"),
    ),
    "cloud architect /engineer ": (
        ("cloud", "architect"),
        ("cloud", "engineer"),
        ("cloud", "ingénieur"),
        ("cloud", "engineer"),
        ("AWS",),
        ("GCP",),
        ("azure",),
    ),
    "solution architect": ("solution", "architect"),
    "big data engineer": (("big", "data", "engineer"), ("ingénieur", "big", "data")),
    "big data developer": (
        ("big", "data", "developer"),
        ("développeur", "big", "data"),
    ),
    "data infrastructure engineer": ("data", "infrastructure", "engineer"),
    "data pipeline engineer": ("data", "pipeline", "engineer"),
    "etl developer": ("etl",),
    "business developer": (("business", "developer"), ("sales", "developer")),
    "business analyst": ("business", "analyst"),
    "cybersecurity": (
        ("cyber", "security"),
        ("cyber", "sécurité"),
        ("cyber", "risk"),
        ("cyber", "risque"),
    ),
    "sysops": ("sysops",),
    "consultant data": ("data", "consultant"),
}

# Dictionnaire des variables et leurs mots-clés correspondants
skills = {
    "ProgLanguage": [
        "Python",
        "Java",
        "C++",
        "C#",
        "Scala",
        " R,",
        "/R/",
        " R ",
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
    "DataAnalytics": ["Pandas", "NumPy", " R,", "/R/", " R ", "MATLAB"],
    "BigData": ["Hadoop", "Spark", "Databricks", "Flink", "Apache Airflow"],
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


# Revoir les intitulés de postes
def find_job_title(title, jobs_dict):
    title_lower = title.lower()

    for job, keywords in jobs_dict.items():
        if any(
            (
                all(word in title_lower for word in keyword_tuple)
                if isinstance(keyword_tuple, tuple)
                else keyword_tuple in title_lower
            )
            for keyword_tuple in keywords
        ):
            return job

    return "Other"


# Fonction pour transformer les exigences d'expérience
def process_experience(experience):
    if experience is None:
        return None 

    experience = experience.lower()

    if "débutant accepté" in experience:
        return "débutant accepté"

    # Chercher d'abord les mois
    mois_match = re.search(r"(\d+)\s*mois", experience)
    if mois_match:
        return f"{mois_match.group(1)} mois"

    # Chercher ensuite les années
    annees_match = re.search(r"(\d+)\s*(?:an|ans|année|années|year|years?)", experience)
    if annees_match:
        return f"{annees_match.group(1)} an(s)"

    # Chercher les expressions avec < ou >
    comparaison_match = re.search(
        r"[<>]\s*(\d+)(?:\s*(?:an|ans|année|années|year|years?))?", experience
    )
    if comparaison_match:
        return f"{comparaison_match.group(1)} an(s)"

    # Chercher simplement un nombre si rien d'autre ne correspond
    nombre_match = re.search(r"\d+", experience)
    if nombre_match:
        return f"{nombre_match.group(0)} an(s)"

    # Si aucun des cas précédents ne correspond, on retourne l'expérience d'origine en minuscules
    return experience


def transform_list_to_string(liste):
    if isinstance(liste, list):
        return ", ".join(liste)
    return liste


# Fonction pour détecter la présence des mots-clés avec des délimiteurs de mots
def find_keywords(description, keywords):
    found_keywords = set()
    description_lower = description.lower()
    for keyword in keywords:
        # Utilisation de \b pour s'assurer que le mot est détecté comme un mot entier
        keyword_lower = keyword.strip().lower()
        if re.search(r"\b" + re.escape(keyword_lower) + r"\b", description_lower):
            found_keywords.add(keyword.strip())
    return list(found_keywords)


# Parcourir chaque fichier JSON dans le dossier
for filename in os.listdir(data_dir):
    if filename.endswith(f"{current_date}.json"):
        filepath = data_dir / filename

        # Lire le fichier JSON
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Appliquer les modifications
        for entry in data:
            # Obtenir le titre et le transformer en job_title, puis supprimer title
            entry["title"] = find_job_title(entry["title"], JOBS) if entry.get("title") else "Other"

            # Ajouter la variable link si elle n'existe pas
            if "link" not in entry:
                entry["link"] = None

            # Transformer experience en liste si ce n'est pas déjà une liste
            if (
                "details" in entry
                and "Experience" in entry["details"]
                and not isinstance(entry["details"]["Experience"], list)
            ):
                entry["details"]["Experience"] = [entry["details"]["Experience"]]

            # Nettoyer et transformer la variable experience si elle est présente
            if "details" in entry and "Experience" in entry["details"]:
                experience_list = entry["details"]["Experience"]
                if isinstance(experience_list, list):
                    transformed_experience = [
                        process_experience(exp) for exp in experience_list
                    ]
                    entry["details"]["Experience"] = ", ".join(
                        set(exp.lower() for exp in transformed_experience if exp)
                    )

            # Remplacer les chaînes de caractères vides par None pour toutes les variables pertinentes dans 'details'
            if "details" in entry:
                for key in ["Experience", "TypeContract", "Salary", "Level"]:
                    if key in entry["details"] and entry["details"][key] == "":
                        entry["details"][key] = None

            # Appliquer la transformation des listes pour les variables concernées (facultatif selon besoin)
            if "details" in entry:
                for key in ["TypeContract", "Salary", "Level"]:
                    if key in entry["details"]:
                        entry["details"][key] = transform_list_to_string(
                            entry["details"][key]
                        )

            # Ajouter la détection des mots-clés pour les skills
            description = entry.get("description", "")
            if description:
                entry["skills"] = {}
                for variable, keywords in skills.items():
                    found_keywords = find_keywords(description, keywords)
                    if found_keywords:
                        entry["skills"][variable] = found_keywords

        # Sauvegarder le fichier JSON modifié
        with open(output_filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

print(f"Les données mises à jour ont été sauvegardées dans {output_filepath}.")
