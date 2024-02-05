'''
This module contains all the constants of the project.
That way, it'll be easily maintainable.
'''

# Liste des constantes
BASEURL = ['https://www.welcometothejungle.com/fr/jobs?query=', 'page=1&aroundQuery=worldwide']
JOBS = ["data engineer",
        "data architect",
        "data scientist",
        "data analyst",
        "software engineer",
        "Data Warehousing Engineer",
        "Machine Learning Engineer",
        "cloud architect",
        "solution architect",
        "cloud engineer",
        "big data engineer",
        "Data Infrastructure Engineer",
        "Data Pipeline Engineer",
        "ETL Developer"]
RACINE_URL = 'https://www.welcometothejungle.com'
JOB_LINK_SELECTOR = '.sc-6i2fyx-0.gIvJqh'
TOTAL_PAGE_SELECTOR = '.sc-bhqpjJ.iCgvlm'
CONTRACT_INFO_SELECTOR = '[data-testid="job-metadata-block"]'
COMPANY_INFO_SELECTOR = '.sc-bXCLTC.dBpdut'
JOB_DESCRIPTION_SELECTOR = '[data-testid="job-section-description"]'
CONTRACT_SELECTORS = {
    'job_title': '.sc-empnci.cYPTxs.wui-text',
    'contract_type': '[name="contract"]',
    'salary': '[name="salary"]',
    'company': '.sc-empnci.hmOCpj.wui-text',
    'location': '[name="location"]',
    'remote': '[name="remote"]',
    'experience': '[name="suitcase"]',
    'education_level': '[name="education_level"]'
}
COMPANY_SELECTORS = {
    'sector': '[alt="Tag"]',
    'company_size': '[alt="Department"]',
    'creation_date': '[alt="Date"]',
    'address': '.sc-ezreuY.iObOsq.sc-boZgaH.fVBQVn.sc-4e9f7k-2.kAeJOl',
    'average_age_of_employees': '[alt="Birthday"]',
    'turnover_in_millions': '[alt="EuroCurrency"]',
    'proportion_female': '[alt="Female"]',
    'proportion_male': '[alt="Male"]'
}
SKILLS_DICT = {
    "Langages de Programmation": [
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
    "Bases de Données": [
        "SQL",
        "NoSQL",
        "MongoDB",
        "Cassandra",
        "Neo4j",
        "HBase",
        "Elasticsearch",
    ],
    "Analyse de Données": ["Pandas", "NumPy", " R,", "/R/", " R ", "MATLAB"],
    "Big Data": ["Hadoop", "Spark", "Databricks", "Flink", "Apache Airflow"],
    "Machine Learning et Data Mining": [
        "Scikit-Learn",
        "TensorFlow",
        "Keras",
        "PyTorch",
        "XGBoost",
        "LightGBM",
        "CatBoost",
        "Orange",
    ],
    "Visualisation de Données": [
        "Tableau",
        "Power BI",
        "Matplotlib",
        "Seaborn",
        "Plotly",
    ],
    "Statistiques": [
        "Statistiques Descriptives",
        "Inférentielles",
        "Bayesian Statistics",
        "Statistiques Bayésiennes",
    ],
    "Cloud Computing": [
        "AWS",
        "Azure",
        "Google Cloud Platform",
        "GCP",
        "IBM Cloud",
        "Alibaba Cloud",
    ],
    "Outils de Développement": ["Git", "Docker", "Jenkins", "Travis CI"],
    "Systèmes d'Exploitation": ["Linux", "Windows", "MacOS"],
    "Bases de Données": [
        "MySQL",
        "PostgreSQL",
        "Oracle SQL",
        "SQL Server",
        "Snowflake",
        "BigQuery",
        "Big Query",
        "SingleStore",
    ],
    "Big Data et Processing": ["Apache Kafka", "Apache Flink", "HBase", "Cassandra"],
    "Automatisation et Orchestration": [
        "Ansible",
        "Kubernetes",
        "Puppet",
        "Chef",
        "Airflow",
    ],
    "Infrastructure as Code (IaC)": ["Terraform", "CloudFormation"],
    "Sécurité et Réseau": ["VPN", "Firewall", "SSL/TLS", "Wireshark"],
    "Virtualisation": ["VMware", "VirtualBox", "Hyper-V"],
    "Containers": ["Docker", "Kubernetes", "OpenShift"],
    "Outils de Collaboration": [
        "JIRA",
        "Confluence",
        "Slack",
        "Microsoft Teams",
        "Teams",
        "Discord",
    ],
    "Compétences": [
        "Big Data",
        "ML",
        "Machine Learning",
        "Statistiques",
        "Cloud",
        "CI/CD",
        "CI / CD",
    ],
}
# OUTPUT_DIR = '/Users/MoG/PycharmProjects/jobmarket/jobmarket'
