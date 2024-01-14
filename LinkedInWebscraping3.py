import pandas as pd 
import parsel as Slector
from time import sleep
from selenium import webdriver

# Import additional packages
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
 
if __name__ == "__main__":
    chrome_driver_path = r'C:\\Users\\Default\\Desktop\\chromedriver-win64\\chromedriver.exe'
    driver = webdriver.Chrome(service=Service(chrome_driver_path))

    # navigate to the given page
    driver.get('https://www.linkedin.com')
    # get the email input field by class_name
    username_field = driver.find_element(By.ID, 'session_key')
    # send the email
    username_field.send_keys('csaid07@live.fr') 
    #sleep for 1 second
    sleep(1)
    # locate password field by class_name
    password_field = driver.find_element(By.ID, 'session_password')
    # send the password
    password_field.send_keys('Avendayer171!')
    #sleep for 1 second
    sleep(1)
    sign_in_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    sign_in_btn.click()
    
    # Get the HTML source code of the page
    html_content = driver.page_source

    # Save the HTML content to a file
    with open('linkedin_page.html', 'w', encoding='utf-8') as file:
        file.write(html_content)

    print('HTML content saved to linkedin_page.html')
    driver.get('https://www.linkedin.com/jobs/search/?currentJobId=3767390645&keywords=data%20engineer%20france&origin=SWITCH_SEARCH_VERTICAL')
    
    # Wait for the search field to be present
    #print("Waiting for the search field to be present...")
    #search_job_field = WebDriverWait(driver, 20).until(
    #    EC.presence_of_element_located((By.CSS_SELECTOR, 'input.search-global-typeahead__input'))
    #)
    #print("Search field is present. Entering 'data engineer'")
    #search_job_field.send_keys('data engineer')

    # Wait for the area field to be present
    #print("Waiting for the area field to be present...")
    #search_job_area_field = WebDriverWait(driver, 20).until(
    #    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.relative #jobs-search-box-location-id-ember30'))
    #)
    #print("Area field is present. Entering 'France'")
    #search_job_area_field.send_keys('France')

    sleep(30)
