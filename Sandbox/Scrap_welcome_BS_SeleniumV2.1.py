# Version avec webdriver simplifié : seule la premiere page de résultat est scrappé
# Pas de saisie pour la location, un seul terme de recherche
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup as bs
import requests 
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# Initialisation du navigateur Chrome via Selenium
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) 

termes = ["data"]

def get_links(url): # Fait la recherche avec le terme puis récupère les liens vers les offres de la premiere page de résultat
    driver.get(url)
    driver.set_window_size(1020, 1020)
    driver.implicitly_wait(3)
    driverjob = driver.find_element(By.ID, "search-query-field") # Cherche le champs de recherche
    driverjob.send_keys(Keys.CONTROL + "a")  # Sélectionne tout le texte dans le champ
    driverjob.send_keys(Keys.DELETE)  # Efface le texte sélectionné
    driverjob.click()
    driverjob.send_keys(termes) # Envoie le terme de recherche
    driverjob.send_keys(Keys.ENTER)
    time.sleep(5)

        
    div_elements = driver.find_elements(By.CLASS_NAME, 'sc-bXCLTC.bAjxyY')
    links = []
    for div_element in div_elements: # Recherche les liens vers les offres
        link_element = div_element.find_element(By.TAG_NAME,'a')
        job_link = link_element.get_attribute('href')
        links.append(job_link)
    for link in links:
        print(link)
    return links
    #number_of_links = len(links)
    #print(f"Nombre de liens récupérés : {number_of_links}")
    
links = get_links('https://www.welcometothejungle.com/fr/')

def get_info(link): # Recupère les infos des offres pour les liens trouvés par get_links
    page = requests.get(link)
    soup = bs(page.text, "lxml")
   
    try : # Nom de l'entreprise
        company_alt = soup.find('img', attrs = {'class' : 'sc-bXCLTC KlSop'})
        company = company_alt.get('alt')
    except :
        company = "N/A"
    try : # Tittre de l'offre
        title = soup.find('h2').text
    except :
        title = "N/A"
    try: # Ensemble d'informations sur l'offre : Type de contrat, lieu, salaire, teletravail, niveau d'étude minimum FIXME : Beaucoup d'offres avec structure différente (pas de job_info_tag))
        job_info_tag = soup.find('div', class_='sc-bXCLTC hdepoj') 
        job_info_texts = [job_info.text for job_info in job_info_tag]
    except:
        contrat = lieu = salaire = teletravail = education = "N/A"
    try:
        contrat = job_info_texts[0]
    except:
        contrat = "N/A"
    try:
        lieu = job_info_texts[1]
    except:
        lieu = "N/A"
    try:
        salaire = job_info_texts[2].replace("Salaire : ","")
    except:
        salaire = "N/A"
    try:
        teletravail = job_info_texts[3]
    except:
        teletravail = "N/A"
    try:
        experience = job_info_texts[4]
    except :
        experience = "N/A"
    try : # date ou heure de publication,
        if soup.find("time").has_attr('datetime'):
            date= soup.find("time").text
    except : 
        date = "N/A"
    try : #experience minimum
        suitcase_icon = soup.find('i', {'name': 'suitcase'})
        education = suitcase_icon.find_next_sibling('span').find_next_sibling('span').text.replace("Éducation : > ", "")
    except :
        education = "N/A"  
    try : # Domaine d'activité
        div_companie = soup.find_all('div', attrs={'data-testid': 'job-company-tag'})
        div_domaine = div_companie[0]
        domaine = div_domaine.find('span').text
    except :    
        domaine = "N/A"
    try : # Taille de l'entreprise
        div_taille = div_companie[1]
        taille = div_taille.find('span').text
    except :
        taille = "N/A"
    #try : # FIXME : trop de N/A
        #profil = soup.find("section", id='profile-section').text
    #except : 
        #profil = "N/A"
    
    line=[company,domaine,taille,lieu,title,date,contrat,teletravail,education,experience,salaire,link]
    return line

info_list = []

for link in links:
    info = get_info(link)
    info_list.append(info)

info_df = pd.DataFrame(info_list, columns=["Company","Domaine","Taille","Lieu","Titre","Date publication","Contrat","teletravail","Education","Experience","Salaire","Link"])
info_df.to_csv('info_emploi.csv', index=False)
print(info_df)

input("Appuyez sur Entrée pour terminer...")