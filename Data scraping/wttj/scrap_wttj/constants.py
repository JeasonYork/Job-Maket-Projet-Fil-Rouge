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
JOB_LINK_SELECTOR = '.sc-1vkc4qv-0.dhhDkN'
TOTAL_PAGE_SELECTOR = '[aria-label="Pagination"]'
CONTRACT_INFO_SELECTOR = '[data-testid="job-metadata-block"]'
COMPANY_INFO_SELECTOR = '.sc-bXCLTC.dBpdut'
JOB_DESCRIPTION_SELECTOR = '[data-testid="job-section-description"]'
CONTRACT_SELECTORS = {
    'job_title': 'h2',
    'contract_type': '[name="contract"]',
    'salary': '[name="salary"]',
    'company': '.sc-bXCLTC.dPVkkc',
    'location': '[name="location"]',
    'remote': '[name="remote"]',
    'experience': '[name="suitcase"]',
    'education_level': '[name="education_level"]'
}
COMPANY_SELECTORS = {
    'sector': '[name="tag"]',
    'company_size': '[name="department"]',
    'creation_date': '[name="date"]',
    'address': '.sc-ezreuY.iObOsq.sc-boZgaH.fVBQVn.sc-4e9f7k-2.kAeJOl',
    'average_age_of_employees': '[name="birthday"]',
    'turnover_in_millions': '[name="euro_currency"]',
    'proportion_female': '[name="female"]',
    'proportion_male': '[male="male"]'
}
RAW_DESCRIPTION_SELECTORS = '.sc-bXCLTC.enCjpg'
SKILLS_DICT = {
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
        "Communication", "Teamwork", "Time Management", "Adaptability", "Problem Solving", "Leadership", "Creativity",
        "Empathy", "Collaboration", "Stress Management", "Organization", "Flexibility", "Initiative",
        "Critical Thinking", "Interpersonal Skills"
    ],
}
# OUTPUT_DIR = '/Users/MoG/PycharmProjects/jobmarket/jobmarket'
