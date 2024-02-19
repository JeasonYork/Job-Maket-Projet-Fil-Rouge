""" Program that loads the France Travail search page and initiates the job search for the defined search terms.
Determines, for each search term, the number of pages based on the number of job offers, then clicks on the "Show the next 20 offers" button as many times as necessary.
For each offer: Extracts data from the search page, then loads the offer page and extracts the remaining data.
Extracts the required skills from the job description.
Option to display the browser or not. """

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import json
from datetime import datetime

base_url = "https://candidat.francetravail.fr/offres/recherche?motsCles={}&offresPartenaires=true&rayon=10&tri=0"

# Definition of local variables
Racine_url = "https://candidat.francetravail.fr/offres/recherche/detail/"
jobs = []
# Data recording file name
filename = "PE_scrapping_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".json"

# List of search terms for web scraping.
Search_term = [
    #"data architect",
    #"data engineer",
    #"data scientist",
    "data analyst",
    #"software engineer",
    #"Data Warehousing Engineer",
    #"Machine Learning Engineer",
    #"cloud architect",
    #"solution architect",
    #"cloud engineer",
    #"big data engineer",
    #"Data Infrastructure Engineer",
    #"Data Pipeline Engineer",
    #"ETL Developer"
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

# Initializing the driver for Google Chrome

#driver = webdriver.Chrome() # Enable navigation display in chrome browser

chrome_options = Options()
chrome_options.add_argument("--headless")  # Enable headless mode (Chrome browser is not displayed)
driver = webdriver.Chrome(options=chrome_options)


def get_total_offers(url):
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
    except Exception as e:
        print("--- Pas de fenetre des cookies - ")

    with open("pole_emploi_04.html", "w", encoding="utf-8") as file:
        file.write(driver.page_source)
    
    try:
        # Find the number of job offers for the search term
        total_offers_element = driver.find_element(By.XPATH, "//div[@id='zoneAfficherListeOffres']//h1[contains(@class, 'title')]")
        total_offers_text = total_offers_element.text
        total_offers = int(total_offers_text.split()[0])
        return total_offers
    except Exception as e:
        print(f"Impossible de trouver le nombre d'offre. Erreur : {e}")
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
            extracted_skills[category] = mentioned_skills

        return extracted_skills
    
def main_process(term):
    # Fetch the total number of offers
    url = base_url.format(term.replace(" ", "+"))
    total_offers = get_total_offers(url)
                
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
                print("Impossible de récuperer la liste totale de résultat")
            
            nb_annonce = 1
            for offer_element in offer_elements:
                # Extraction of offer data from the results page.
                try:
                    Job_ref = offer_element.get_attribute('data-id-offre')
                except:
                    Job_ref = "N/A"
                try:
                    Job_url = Racine_url + Job_ref
                except:
                    Job_url = "N/A"
                try:
                    job_title = offer_element.find_element(By.CSS_SELECTOR, 'h2[data-intitule-offre]').text
                except:
                    job_title = "N/A"
                try:
                    company_location_element = offer_element.find_element(By.CSS_SELECTOR, 'p.subtext')
                    company_and_location = company_location_element.text.split(' - ')
                    Company = company_and_location[0]
                    Location = company_and_location[1]
                    if Company.isdigit():
                        Location += ' ' + Company
                        Company = 'N/A'
                    Full_contract_type = offer_element.find_element(By.CSS_SELECTOR, 'div.media-right.media-middle.hidden-xs p.contrat').text
                    Contract_type = Full_contract_type.split()[0]
                except:
                    Company = Location = "N/A"
                try:
                    Full_contract_type = offer_element.find_element(By.CSS_SELECTOR, 'div.media-right.media-middle.hidden-xs p.contrat').text
                    Contract_type = Full_contract_type.split()[0]
                except:
                    Contract_type = "N/A"
                try :
                    Date = offer_element.find_element(By.CSS_SELECTOR, 'p.date').text
                except :
                    Date = "N/A"
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
                    salary = "N/A"
                try:
                    experience = driver.find_element(By.CSS_SELECTOR, 'span[itemprop="experienceRequirements"].skill-name').text
                except:
                    experience = "N/A"
                try:
                    education_level = driver.find_element(By.CSS_SELECTOR, 'span[itemprop="educationRequirements"].skill-name').text
                except:
                    education_level = "N/A"
                try:
                    description = driver.find_element(By.CSS_SELECTOR, 'div.description.col-sm-8.col-md-7').text
                except:
                    description = "N/A"

                extracted_skills = extract_skills(description)

                driver.close()
                driver.switch_to.window(main_window)
                job = {
                    "title": job_title,
                    "company": Company,
                    "Location": Location,
                    "link": Job_url,
                    "TypeContract": Contract_type,
                    "Salary": salary,
                    "Level": education_level,
                    "Experience": experience,
                    "description": description,
                    "skills": extracted_skills,
                    "PublicationDate": Date,
                    "SearchTerm": term,
                    "JobReference": Job_ref
                }
                jobs.append(job)

                """ # Enregistrement des données
                with open(filename, 'a', encoding='utf-8') as f:
                    json.dump(job, f, ensure_ascii=False)
                    f.write('\n') """

                print("Annonce", nb_annonce,"sur", total_offers,  Job_url, "OK")
                job = {}
                nb_annonce+=1
                time.sleep(3)          
        else:
            print("Erreur lors du clic sur le bouton.")
    else:
        print("Impossible d'obtenir le nombre total d'annonces.")

if __name__ == "__main__":
    for term in Search_term:
        main_process(term)
    
    # Data recording
        with open(filename, 'a', encoding='utf-8') as f:
            json.dump(jobs, f, ensure_ascii=False)
            f.write('\n')
        print("********* Enregistrement des données : ", filename)
        jobs = []

print("Scrapping France Travail terminé")

        