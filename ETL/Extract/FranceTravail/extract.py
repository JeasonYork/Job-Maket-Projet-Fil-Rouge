from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import os
from transform import transform_date
from datetime import datetime

base_url = "https://candidat.francetravail.fr/offres/recherche?motsCles={}&offresPartenaires=true&rayon=10&tri=0"
Racine_url = "https://candidat.francetravail.fr/offres/recherche/detail/"

def log_scraping_results(log_file_path, term, num_jobs):
    num_jobs -= 1
    with open(log_file_path, 'a') as log_file:
        log_entry = f"{datetime.now().strftime('%Y%m%d_%H%M%S')} - Term: {term} - Jobs added: {num_jobs}\n"
        log_file.write(log_entry)

def get_total_offers(driver, url, collect_all):
    driver.get(url)
    time.sleep(8)
    wait = WebDriverWait(driver, 10)

    try:
        pe_cookies_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "pe-cookies")))
        shadow = driver.execute_script('return arguments[0].shadowRoot', pe_cookies_element)
        button_inside_shadow = shadow.find_element(By.ID, "pecookies-accept-all")
        button_inside_shadow.click()
        time.sleep(5)
    except Exception as e:
        print("--- No cookies window found ---")

    if not collect_all:
        try:
            driver.find_element(By.CSS_SELECTOR, "#filter-date-creation").click()
            time.sleep(3)
            driver.find_element(By.CSS_SELECTOR, ".radio:nth-child(1) > .control-label").click()
            time.sleep(3)
            driver.find_element(By.CSS_SELECTOR, "#btnSubmitDateCreation").click()
            time.sleep(5)
            print("Filter 'Un jour' selected")
        except:
            print("Could not apply 'Un jour' filter")

    try:
        total_offers_element = driver.find_element(By.XPATH, "//div[@id='zoneAfficherListeOffres']//h1[contains(@class, 'title')]")
        total_offers_text = total_offers_element.text
        total_offers = int(total_offers_text.split()[0])
        return total_offers
    except Exception as e:
        print("Could not find the number of offers.")
        return None

def click_show_more_offers(driver, times_to_click):
    try:
        for n in range(times_to_click):
            print("Loading page", n+1, "of", times_to_click)
            show_more_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//p[@class='results-more text-center']//a[@role='button']"))
            )
            show_more_button.click()
            time.sleep(4)
        return True
    except Exception as e:
        print(f"Error while clicking the button: {e}")
        return False

def scraping_and_process(term, driver, json_scraping_directory, log_file_path, collect_all=False):
    nb_annonce = 0

    url = base_url.format(term.replace(" ", "+"))
    total_offers = get_total_offers(driver, url, collect_all)

    if total_offers is not None:
        print(f"{term} - Total job offers: {total_offers}")

        clicks_needed = (total_offers // 20)
        if clicks_needed > 49:
            print("(More than 49 pages to load)", clicks_needed)
            clicks_needed = 49
        print(f'Pages to load: {clicks_needed}')
        click_result = click_show_more_offers(driver, clicks_needed)

        if click_result:
            if clicks_needed != 0:
                print(f"'Show more offers' button clicked successfully {clicks_needed} times.")
            print("Starting scraping")
            try:
                offer_elements = driver.find_elements(By.CSS_SELECTOR, 'li.result')
            except:
                print("Unable to retrieve the result list")

            jobs = []
            nb_annonce = 1
            for offer_element in offer_elements:
                # Extract job data from the results page.
                job = extract_job_data(offer_element, driver)
                if job:
                    jobs.append(job)
                    save_job_data(job, term, json_scraping_directory)
                    print("Ad", nb_annonce, "out of", total_offers, job["link"], "OK")
                    nb_annonce += 1
                    time.sleep(2)

            log_scraping_results(log_file_path, term, nb_annonce)
        else:
            print("Error while clicking the button.")
    else:
        print("Unable to get the total number of ads.")

def extract_job_data(offer_element, driver):
    job = {}
    try:
        Job_ref = offer_element.get_attribute('data-id-offre')
        Job_url = Racine_url + Job_ref
        job["link"] = Job_url
    except:
        return None

    try:
        job["title"] = offer_element.find_element(By.CSS_SELECTOR, 'h2[data-intitule-offre]').text
    except:
        job["title"] = None

    try:
        company_location_element = offer_element.find_element(By.CSS_SELECTOR, 'p.subtext')
        company_and_location = company_location_element.text.split(' - ')
        job["company"] = company_and_location[0]
        job["location"] = company_and_location[1]
    except:
        job["company"] = job["location"] = None

    try:
        job["details"] = {
            "TypeContract": offer_element.find_element(By.CSS_SELECTOR, 'div.media-right.media-middle.hidden-xs p.contrat').text.split()[0],
            "Salary": driver.find_element(By.CSS_SELECTOR, 'ul[style="list-style-type: none; margin:0; padding: 0"] li').text,
            "Experience": driver.find_element(By.CSS_SELECTOR, 'span[itemprop="experienceRequirements"].skill-name').text,
            "Level": driver.find_element(By.CSS_SELECTOR, 'span[itemprop="educationRequirements"].skill-name').text,
        }
    except:
        job["details"] = None

    try:
        job["publication_date"] = transform_date(offer_element.find_element(By.CSS_SELECTOR, 'p.date').text)
    except:
        job["publication_date"] = None

    try:
        job["description"] = driver.find_element(By.CSS_SELECTOR, 'div.description.col-sm-8.col-md-7').text
        job["company_data"] = {
            "sector": driver.find_element(By.CSS_SELECTOR, 'span[itemprop="industry"]').text,
            "company_size": driver.find_element(By.CSS_SELECTOR, 'div.media > div.media-body > p').text,
        }
    except:
        job["description"] = None
        job["company_data"] = None

    return job

def save_job_data(job, term, json_scraping_directory):
    time_file = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(json_scraping_directory, "FT_scrapping_" + time_file + "_" + term + ".json")
    file_exists = os.path.isfile(filename)
    if not file_exists or os.stat(filename).st_size == 0:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump([job], f, ensure_ascii=False, indent=4)
    else:
        with open(filename, 'r+', encoding='utf-8') as f:
            f.seek(0, os.SEEK_END)
            f.seek(f.tell() - 1, os.SEEK_SET)
            if f.tell() > 1:
                f.write(', ')
            else:
                f.seek(0, os.SEEK_SET)
                f.write('[')
            json.dump(job, f, ensure_ascii=False, indent=4)
            f.write(']')
