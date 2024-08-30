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
JOB_LINK_SELECTOR = 'div.sc-1gjh7r6-7.fCBkLE > a'
TOTAL_PAGE_SELECTOR = '[aria-label="Pagination"]'
CONTRACT_INFO_SELECTOR = '[data-testid="job-metadata-block"]'
COMPANY_INFO_SELECTOR = '.sc-bXCLTC.dBpdut'
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
    'turnover_in_millions': '[name="euro_currency"]',
}
RAW_DESCRIPTION_SELECTORS = '.sc-bXCLTC.enCjpg'
# OUTPUT_DIR = '/Users/MoG/PycharmProjects/jobmarket/jobmarket'
