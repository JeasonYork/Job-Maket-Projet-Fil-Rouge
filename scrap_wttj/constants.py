'''
This module contains all the constants of the project.
That way, it'll be easily maintainable.
'''


# Liste des constantes
BASEURL = 'https://www.welcometothejungle.com/fr/jobs?query=data%20engineer&page=1&aroundQuery=worldwide'
RACINE_URL = 'https://www.welcometothejungle.com'
JOB_LINK_SELECTOR = '.sc-6i2fyx-0.gIvJqh'
TOTAL_PAGE_SELECTOR = '.sc-bhqpjJ.iCgvlm'
CONTRACT_INFO_SELECTOR = '.sc-bXCLTC.jlqIpd.sc-fbKhjd.kfysmu.sc-1wwpb2t-5.hexbEF'
COMPANY_INFO_SELECTOR = '.sc-bXCLTC.dBpdut'
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
# OUTPUT_DIR = '/Users/MoG/PycharmProjects/jobmarket/jobmarket'
