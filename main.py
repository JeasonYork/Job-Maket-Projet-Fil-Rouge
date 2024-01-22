#Programme qui charge la page de recherche de France Travail.
#Determine le nombre de page en fonction du nombre d'offres, puis clique sur le bouton "Afficher les 20 offres suivantes" le nombre de fois necessaire.
#Pour chaques offres : Extrait les données de la page de recherche, puis charge la page de l'offre et extrait les données restantes.
#Affiche le navigateur.
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import csv
from datetime import datetime

Base_url = "https://candidat.pole-emploi.fr/offres/recherche?motsCles=data+engineer&offresPartenaires=true&rayon=10&tri=0"
Racine_url = "https://candidat.pole-emploi.fr/offres/recherche/detail/"
jobs = []
nb_annonce = 1

# Instancier le navigateur web
driver = webdriver.Chrome()

def get_total_offers(url):
    # Charger la page
    driver.get(url)
    time.sleep(10)
    wait = WebDriverWait(driver, 10)
     #fermeture de la fenetre cookies
    try:
        pe_cookies_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "pe-cookies")))
        shadow = driver.execute_script('return arguments[0].shadowRoot', pe_cookies_element) # Obtenir l'ombre DOM
        button_inside_shadow = shadow.find_element(By.ID, "pecookies-accept-all")
        button_inside_shadow.click()
        print(" --- cookies fermés ---")
    except Exception as e:
        print("Problème lors de la fermeture de la fenetre cookies")

    with open("pole_emploi_02.html", "w", encoding="utf-8") as file:
        file.write(driver.page_source)
    
    try:
        #Nombre total d'offres
        total_offers_element = driver.find_element(By.XPATH, "//div[@id='zoneAfficherListeOffres']//h1[contains(@class, 'title')]")
        total_offers_text = total_offers_element.text
        total_offers = int(total_offers_text.split()[0])  # Extraire le nombre comme un entier
        return total_offers
    except Exception as e:
        print(f"Impossible de trouver le nombre d'offre. Erreur : {e}")
        return None

def click_show_more_offers(driver, times_to_click):
    try:
        for n in range(times_to_click):
            # Trouver et cliquer sur l'élément du bouton "Afficher les 20 offres suivantes"
            print("Chargement de la page d'annonces ", n+1, "sur ", times_to_click)
            show_more_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//p[@class='results-more text-center']//a[@role='button']"))
            )
            show_more_button.click()
            time.sleep(5)
        return True
    except Exception as e:
        print(f"Une erreur s'est produite lors du clic sur le bouton : {e}")
        return False

# Récuperer le nombre total d'annonces
total_offers = get_total_offers(Base_url)

if total_offers is not None:
    print(f"Nombre total d'annonces : {total_offers}")

    # Calculez le nombre de clics nécessaires
    clicks_needed = (total_offers // 20)
    print(f'Nombre de pages à charger : {clicks_needed}')

    # Cliquez sur le bouton "Afficher les 20 offres suivantes" plusieurs fois
    click_result = click_show_more_offers(driver, clicks_needed)

    if click_result:
        print(f"Bouton cliqué avec succès {clicks_needed} fois.")
        
        try:
            offer_elements = driver.find_elements(By.CSS_SELECTOR, 'li.result')
        except:
            print("Impossible de récuperer la liste totale de résultat")

        for offer_element in offer_elements:
            # Extraction des données de l'offre dans la page de résultats
            Job_ref = offer_element.get_attribute('data-id-offre')
            Job_url = Racine_url + Job_ref
            job_title = offer_element.find_element(By.CSS_SELECTOR, 'h2[data-intitule-offre]').text
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
                Date = offer_element.find_element(By.CSS_SELECTOR, 'p.date').text
            except:
                Company = Location = Contract_type = Date = "N/A"

            main_window = driver.current_window_handle
            driver.execute_script("window.open();")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(Job_url)

            try:
                salary = salary_element = driver.find_element(By.CSS_SELECTOR, 'ul[style="list-style-type: none; margin:0; padding: 0"] li').text
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
                skills_elements = driver.find_elements(By.CSS_SELECTOR, 'span[itemprop="skills"].skill-name')
                skills = [skill_element.text for skill_element in skills_elements]
            except :
                skills = "N/A"
            try:
                description = driver.find_element(By.CSS_SELECTOR, 'div.description.col-sm-8.col-md-7').text
            except:
                description = "N/A"

            driver.close()
            driver.switch_to.window(main_window)
            job = {
                "Job reference": Job_ref,
                "Job title": job_title,
                "Date de publication": Date,
                "Company": Company,
                "Location": Location,
                "Contract type": Contract_type,
                "URL": Job_url,
                "Salary": salary,
                "Experience": experience,
                "Education level": education_level,
                "Skills": skills,
                "Description": description
            }
            jobs.append(job)
            print("Annonce", nb_annonce, Job_url, "OK")
            nb_annonce+=1
            time.sleep(3)

        # Enregistrement des données
        filename = "PE_database_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(jobs, f, ensure_ascii=False)
        print("Enregistrement des données : ", filename)
        filename = "PE_database_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".csv"
        with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=jobs[0].keys())
            writer.writeheader()
            writer.writerows(jobs)
        print("Enregistrement des données : ", filename)

    else:
        print("Erreur lors du clic sur le bouton.")
else:
    print("Impossible d'obtenir le nombre total d'annonces.")