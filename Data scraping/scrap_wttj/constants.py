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
TOTAL_PAGE_SELECTOR = '[aria-label="Pagination"]'
CONTRACT_INFO_SELECTOR = '[data-testid="job-metadata-block"]'
COMPANY_INFO_SELECTOR = '.sc-bXCLTC.dBpdut'
JOB_DESCRIPTION_SELECTOR = '[data-testid="job-section-description"]'
CONTRACT_SELECTORS = {
    'job_title': '.sc-bdOgaJ.kEoFYF',
    'contract_type': '[name="contract"]',
    'salary': '[name="salary"]',
    'company': '.sc-bdOgaJ.kaknoe',
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
    "programming_languages": [
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
    "databases": [
        "SQL",
        "NoSQL",
        "MongoDB",
        "Cassandra",
        "Neo4j",
        "HBase",
        "Elasticsearch",
    ],
    "data_analyze": ["Pandas", "NumPy", " R,", "/R/", " R ", "MATLAB"],
    "big_data_tools": ["Hadoop", "Spark", "Databricks", "Flink", "Apache Airflow"],
    "ML_and_data_mining": [
        "Scikit-Learn",
        "TensorFlow",
        "Keras",
        "PyTorch",
        "XGBoost",
        "LightGBM",
        "CatBoost",
        "Orange",
    ],
    "data_viz": [
        "Tableau",
        "Power BI",
        "Matplotlib",
        "Seaborn",
        "Plotly",
    ],
    "statistics": [
        "Statistiques Descriptives",
        "Inférentielles",
        "Bayesian Statistics",
        "Statistiques Bayésiennes",
    ],
    "cloud_computing": [
        "AWS",
        "Azure",
        "Google Cloud Platform",
        "GCP",
        "IBM Cloud",
        "Alibaba Cloud",
    ],
    "dev_tools": ["Git", "Docker", "Jenkins", "Travis CI"],
    "OS": ["Linux", "Windows", "MacOS"],
    "databases": [
        "MySQL",
        "PostgreSQL",
        "Oracle SQL",
        "SQL Server",
        "Snowflake",
        "BigQuery",
        "Big Query",
        "SingleStore",
    ],
    "big_data_and_processing": ["Apache Kafka", "Apache Flink", "HBase", "Cassandra"],
    "automation_and_orchestration": [
        "Ansible",
        "Kubernetes",
        "Puppet",
        "Chef",
        "Airflow",
    ],
    "IaC": ["Terraform", "CloudFormation"],
    "security_and_network": ["VPN", "Firewall", "SSL/TLS", "Wireshark"],
    "virtualization": ["VMware", "VirtualBox", "Hyper-V"],
    "containers": ["Docker", "Kubernetes", "OpenShift"],
    "collaboration": [
        "JIRA",
        "Confluence",
        "Slack",
        "Microsoft Teams",
        "Teams",
        "Discord",
    ],
    "skills": [
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
