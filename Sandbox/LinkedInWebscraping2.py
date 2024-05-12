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

opts = Options()

chrome_driver_path = r'C:\\Users\\Default\\Desktop\\chromedriver-win64\\chromedriver.exe'
service = Service(chrome_driver_path)

driver = webdriver.Chrome(service=service, options=opts)

#check if all data keys have a value
def validate_fiels(filed):
    if field:
        pass
    else:
        filed = 'No results'
    return filed

# navigate to the given page
driver.get('https://www.linkedin.com')

# get the email input field by class_name
username = driver.find_element(By.ID, 'session_key')

# send the email
username.send_keys('csaid07@live.fr')

#sleep for 1 second
sleep(1)

# locate password field by class_name
password = driver.find_element(By.ID, 'session_password')

# send the password
password.send_keys('Avendayer171!')
sleep(1)

# locate submit button by xpath
sing_in_button = driver.find_element(By.XPATH, '//*[@type="submit"]')

# click to the button
sing_in_button.click()
sleep(15)

Jobdata = []
links = []
for x in range(0, 20, 10):
    driver.get(f'https://www.google.fr/search?q=data+engineer+france&sca_esv=597031683&sxsrf=ACQVn08-Keab11N6U2uYzYdhxElxwZWZ_g%3A1704840954641&source=hp&ei=-s6dZfKFJfGoxc8P8fy38AE&iflsig=ANes7DEAAAAAZZ3dCsHMURgzvXzeyDBfl055DzqtI3OJ&oq=data+engineer+fran&gs_lp=Egdnd3Mtd2l6IhJkYXRhIGVuZ2luZWVyIGZyYW4qAggAMgUQABiABDIGEAAYFhgeMgYQABgWGB4yBhAAGBYYHjIGEAAYFhgeMgYQABgWGB4yBhAAGBYYHjIGEAAYFhgeMgYQABgWGB4yBhAAGBYYHkj2WFCaA1inRXABeACQAQCYAWSgAa8GqgEDOC4xuAEByAEA-AEBqAIKwgIHECMY6gIYJ8ICChAjGIAEGIoFGCfCAhEQLhiABBixAxiDARjHARjRA8ICCxAAGIAEGLEDGIMBwgIOEAAYgAQYigUYsQMYgwHCAgsQLhiABBixAxiDAcICDhAuGIAEGIoFGLEDGIMBwgIIEAAYgAQYsQPCAgoQABiABBgUGIcC&sclient=gws-wiz')
    time.sleep(random.uniform(2.5, 4.9))
    linkedin_urls = [my_elem.get_attribute('href') for my_elem in WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'your_css_selector_here')))]



