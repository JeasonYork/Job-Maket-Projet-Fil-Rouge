""" Program that loads the France Travail search page and initiates the job search for the defined search terms.
Determines, for each search term, the number of pages based on the number of job offers, then clicks on the "Show the next 20 offers" button as many times as necessary.
For each offer: Extracts data from the search page, then loads the offer page and extracts the remaining data.
Extracts the required skills from the job description.

Option to display the browser (firefox or chrome) or not.

Command line argument '--all' : allow the script to retrieve all aoffers without any date restrictions.
No argument : applies a filter for 'the last 3 days'
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
import argparse
import time
import json
import os
from datetime import datetime

start_time = time.time()
base_url = "https://candidat.francetravail.fr/offres/recherche?motsCles={}&offresPartenaires=true&rayon=10&tri=0"

# Definition of local variables
Racine_url = "https://candidat.francetravail.fr/offres/recherche/detail/"
jobs = []
# Data recording file name
time_file = datetime.now().strftime("%Y%m%d_%H%M%S")
time_offer = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

#filename = "PE_scrapping_" + time_file + ".json"

# Chemin du dossier JSON_AUTO
current_directory = os.path.dirname(os.path.realpath(__file__))
json_auto_directory = os.path.join(current_directory, "JSON_AUTO")
if not os.path.exists(json_auto_directory):
    os.makedirs(json_auto_directory)

# List of search terms for web scraping.
Search_term = [
    "data architect",
    "data engineer",
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
    "ETL Developer"
]
# Dictionary of skills and their associated skills categories.
skill_categories = {
        "ProgLanguage": ("Python", "Java", "C++", "C#", "Scala", "R", " R ", "/R/", "Julia", "Go", "Kotlin", "Bash", "JavaScript", "HTML"),
        "DataBase": ("SQL", "NoSQL", " MongoDB", "Cassandra", "Neo4j", "HBase", "Elasticsearch"),
        "DataAnalytics": ("Pandas", "NumPy", "R", " R ", "/R/", "MATLAB"),
        "BigData": ("Hadoop", "Spark", "Databricks", "Flink", "Apache Airflow"),
        "MachingLearning": ("Scikit-Learn", "TensorFlow", "Keras", "PyTorch", "XGBoost", "LightGBM", "CatBoost", "Orange"),
        "DataSerialization" : ("Avro","Protocol Buffers","Json","XML"),
        "DataVisualization": ("Tableau", "Power BI", "PowerBI", "Matplotlib", "Seaborn", "Plotly"),
        "Statistics": ("Statistics", "Statistiques", "Statistiques Descriptives", "Inférentielles", "Bayesian Statistics", "Statistiques Bayésiennes"),
        "CloudComputing": ("AWS", "Azure", "Google Cloud Platform", "IBM Cloud", "Alibaba Cloud"),
        "DevTools": ("Git", "Docker", "Jenkins", "Travis CI"),
        "Os": ("Linux", "Windows", "MacOS"),
        "DBMS": ("MySQL", "PostgreSQL", "Oracle", "SQL Server", "Snowflake", "Snowflake","BigQuery","Big Query","SingleStore"),
        "SoftBigDataProcessing": ("Apache Kafka", "Apache Flink", "HBase", "Apache Cassandra"),
        "Automation": ("Ansible", "Kubernetes", "Puppet", "Chef", "Airflow"),
        "InfrastructureAsCode": ("Terraform", "CloudFormation"),
        "NetworkSecurty": ("VPN", "Firewall", "SSL/TLS", "Wireshark"),
        "Virtualisation": ("VMware", "vSphere", "VirtualBox", "Hyper-V"),
        "Containers": ("Docker", "Kubernetes", "OpenShift"),
        "Collaboration": ("JIRA", "Confluence", "Slack", "Microsoft Teams", "Discord", "Teams"),
        "Other": ("DevOps","Backend Development","Big Data","ML","Machine Learning","Statistiques","Cloud","CI/CD","CI / CD"),
        "FrSoftSkills": ("Communication","Travail d'équipe","Gestion du temps","Adaptabilité","Résolution de problèmes","Leadership" ,"Créativité","Empathie","Collaboration","Gestion du stress","Organisation","Flexibilité","Esprit d'initiative","Pensée critique","Relations interpersonnelles"),
        "EnSoftSkils": ("Communication","Teamwork","Time Management","Adaptability","Problem Solving","Leadership","Creativity","Empathy","Collaboration","Stress Management","Organization","Flexibility","Initiative","Critical Thinking","Interpersonal Skills"),
        }

def initialize_driver():
    #gecko_driver_path = "/usr/bin/geckodriver"
    #firefox_service = FirefoxService(executable_path=gecko_driver_path)
    #firefox_options = Options()  # Utilisez FirefoxOptions pour configurer les options spécifiques à Firefox
    #firefox_options.headless = True  # Exécution sans interface graphique = True
    #driver = webdriver.Firefox(service=firefox_service, options=firefox_options)
    #return driver
# Initializing the driver for Google Chrome

    #driver = webdriver.Chrome() # Enable navigation display in chrome browser
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Enable headless mode (Chrome browser is not displayed)
    driver = webdriver.Chrome(options=chrome_options)
    return driver

# Initializing the driver for firefox Chrome



def get_total_offers(url, collect_all):
    # Charger la page
    driver.get(url)
    time.sleep(10) # TO TEST
    wait = WebDriverWait(driver, 10)
    #fermeture de la fenetre cookies
    try:
        pe_cookies_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "pe-cookies")))
        shadow = driver.execute_script('return arguments[0].shadowRoot', pe_cookies_element) # Obtenir l'ombre DOM
        button_inside_shadow = shadow.find_element(By.ID, "pecookies-accept-all")
        button_inside_shadow.click()
        print(" --- cookies fermés ---")
        time.sleep(5)
    except Exception as e:
        print("--- Pas de fenetre des cookies - ")

    # Click on 'Date de creation' then 'Trois jours'
    if not collect_all:
        try:
            driver.find_element(By.CSS_SELECTOR, "#filter-date-creation").click()
            time.sleep(3)
            driver.find_element(By.CSS_SELECTOR, ".radio:nth-child(2) > .control-label").click()
            time.sleep(3)
            driver.find_element(By.CSS_SELECTOR, "#btnSubmitDateCreation").click()
            time.sleep(5)
            print("Filtre 'Trois jours' selectionné")
        except:
            print("impossible d'appliquer le filtre 'Trois jours' ")
        
    try:
        # Find the number of job offers for the search term
        total_offers_element = driver.find_element(By.XPATH, "//div[@id='zoneAfficherListeOffres']//h1[contains(@class, 'title')]")
        total_offers_text = total_offers_element.text
        total_offers = int(total_offers_text.split()[0])
        return total_offers
    except Exception as e:
        print(f"-{term} Impossible de trouver le nombre d'offre.")
        return None

def click_show_more_offers(driver, times_to_click):
    try:
        for n in range(times_to_click):
            # Find and click on the "Show next 20 offers" button item
            print("Chargement de la page d'annonces ", n+1, "sur ", times_to_click)
            show_more_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//p[@class='results-more text-center']//a[@role='button']"))
            )
            show_more_button.click()
            time.sleep(4)
        return True
    except Exception as e:
        print(f"Une erreur s'est produite lors du clic sur le bouton : {e}")
        return False
    
def extract_skills(description: str) -> dict:
        """
        Extract skills from a job description and categorize them into skill groups.

        Args:
            description (str): The job description text.

        Returns:
            dict: A dictionary containing skill groups with their respective skills.
        """
        extracted_skills = {category: [] for category in skill_categories}

        # Iterate over each skill category
        for category, skills in skill_categories.items():
            # Check if any skill in the category is mentioned in the description
            mentioned_skills = [skill for skill in skills if skill.lower() in description.lower()]

            # Append mentioned skills to the corresponding category list
            if mentioned_skills:
                extracted_skills[category] = mentioned_skills
            else:
                extracted_skills[category] = None

        return extracted_skills
    
def scraping_and_process(term, driver, collect_all=False):
    # Fetch the total number of offers
    url = base_url.format(term.replace(" ", "+"))
    total_offers = get_total_offers(url, collect_all)
                
    if total_offers is not None:
        print(f"{term} - Nombre total d'annonces : {total_offers}")

        # Click the necessary number of times to display all offers.

        clicks_needed = (total_offers // 20)
        print(f'Nombre de pages à charger : {clicks_needed}')
        click_result = click_show_more_offers(driver, clicks_needed)

        if click_result:
            print(f"Bouton 'show more offers' cliqué avec succès {clicks_needed} fois.")
            
            try:
                offer_elements = driver.find_elements(By.CSS_SELECTOR, 'li.result')
            except:
                print("Impossible de récuperer la liste de résultat")
            
            nb_annonce = 1
            for offer_element in offer_elements:
                # Extraction of offer data from the results page.
                try:
                    Job_ref = offer_element.get_attribute('data-id-offre')
                except:
                    Job_ref = None
                try:
                    Job_url = Racine_url + Job_ref
                except:
                    Job_url = None
                try:
                    job_title = offer_element.find_element(By.CSS_SELECTOR, 'h2[data-intitule-offre]').text
                except:
                    job_title = None
                try:
                    company_location_element = offer_element.find_element(By.CSS_SELECTOR, 'p.subtext')
                    company_and_location = company_location_element.text.split(' - ')
                    Company = company_and_location[0]
                    Location = company_and_location[1]
                    if Company.isdigit():
                        Location += ' ' + Company
                        Company = None
                    Full_contract_type = offer_element.find_element(By.CSS_SELECTOR, 'div.media-right.media-middle.hidden-xs p.contrat').text
                    Contract_type = Full_contract_type.split()[0]
                except:
                    Company = Location = None
                try:
                    Full_contract_type = offer_element.find_element(By.CSS_SELECTOR, 'div.media-right.media-middle.hidden-xs p.contrat').text
                    Contract_type = Full_contract_type.split()[0]
                except:
                    Contract_type = None
                try :
                    Date = offer_element.find_element(By.CSS_SELECTOR, 'p.date').text
                except :
                    Date = None
                # Load the link to the offer in a new tab
                main_window = driver.current_window_handle
                driver.execute_script("window.open();")
                driver.switch_to.window(driver.window_handles[1])
                try :
                    driver.get(Job_url)
                except :
                    print("erreur dans l'URL")
                    break

                try:
                    salary = driver.find_element(By.CSS_SELECTOR, 'ul[style="list-style-type: none; margin:0; padding: 0"] li').text
                except:
                    salary = None
                try:
                    experience = driver.find_element(By.CSS_SELECTOR, 'span[itemprop="experienceRequirements"].skill-name').text
                except:
                    experience = None
                try:
                    education_level = driver.find_element(By.CSS_SELECTOR, 'span[itemprop="educationRequirements"].skill-name').text
                except:
                    education_level = None
                try:
                    description = driver.find_element(By.CSS_SELECTOR, 'div.description.col-sm-8.col-md-7').text
                except:
                    description = None
                try:
                    sector = driver.find_element(By.CSS_SELECTOR, 'span[itemprop="industry"]').text
                except:
                    sector = None
                try:
                    company_size = driver.find_element(By.CSS_SELECTOR, 'div.media > div.media-body > p').text
                except:
                    company_size = None
                extracted_skills = extract_skills(description)

                driver.close()
                driver.switch_to.window(main_window)
                job = {
                    "job_title": job_title,
                    "contract_type": Contract_type,
                    "salary": salary,
                    "company": Company,
                    "location": Location,
                    "experience": experience,
                    "education_level": education_level,
                    "publication_date": Date,
                    "sector": sector,
                    "company_size": company_size,
                    "link": Job_url,                    
                    "skills": extracted_skills,
                    "search_term": term,
                    "job_reference": Job_ref,
                    "raw_description": description,
                    "createdAt": time_offer
                }
                jobs.append(job)

                # Enregistrement des données
                #filename = "PE_scrapping_" + time_file + "_" + term + ".json"
                filename = os.path.join(json_auto_directory, "PE_scrapping_" + time_file + "_" + term + ".json")
                #with open(filename, 'a', encoding='utf-8') as f:
                    #json.dump(job, f, ensure_ascii=False)
                    #f.write('\n')
                file_exists = os.path.isfile(filename)
                if not file_exists or os.stat(filename).st_size == 0:
                    with open(filename, 'w', encoding='utf-8') as f:
                    # Pour le premier job, écrire une liste ouvrante et le job
                        json.dump([job], f, ensure_ascii=False, indent=4)
                else:
                    with open(filename, 'r+', encoding='utf-8') as f:
                        f.seek(0, os.SEEK_END)  # Allez à la fin du fichier
                        f.seek(f.tell() - 1, os.SEEK_SET)  # Reculer de 1 pour enlever le crochet fermant ']'
                        # Si fichier vide ou contient seulement '[]'
                        if f.tell() > 1:
                            f.write(', ')  # Écrire une virgule avant d'ajouter le nouvel objet
                        else:
                            f.seek(0, os.SEEK_SET)  # Retour au début du fichier pour écrire le premier objet
                            f.write('[')
                        json.dump(job, f, ensure_ascii=False, indent=4)
                        f.write(']')  # Ajoutez le crochet fermant pour clôturer le tableau JSON
                        
                print("Annonce", nb_annonce,"sur", total_offers,  Job_url, "OK")
                job = {}
                nb_annonce+=1
                time.sleep(2) #TOTEST          
        else:
            print("Erreur lors du clic sur le bouton.")
    else:
        print("Impossible d'obtenir le nombre total d'annonces.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape job offers from France Travail.")
    parser.add_argument("--all", action='store_true', help="Collect all offers without date filtering.")
    #parser.add_argument("--browser", type=str, default="chrome", help="Type of browser to use ('chrome' or 'firefox').")
    args = parser.parse_args()

    driver = initialize_driver()
    for term in Search_term:
        scraping_and_process(term, driver, collect_all=args.all)
        
    
    """ # Data recording
        with open(filename, 'a', encoding='utf-8') as f:
            json.dump(jobs, f, ensure_ascii=False)
            f.write('\n')
        print("********* Enregistrement des données : ", filename)
        jobs = [] """
end_time = time.time()
execution_time = end_time - start_time
minutes, seconds = divmod(execution_time, 60)
print("Scrapping France Travail terminé")

print("Durée d'exécution :", int(execution_time), "secondes ({} minutes et {} secondes)".format(int(minutes), int(seconds)))

        