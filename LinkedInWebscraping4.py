from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import math
import time

# Set up ChromeOptions
options = Options()
options.add_argument("--headless")  # Run Chrome in headless mode (without a GUI)

# Specify the path to your chromedriver executable
chrome_driver_path = r'C:\\Users\\Default\\Desktop\\chromedriver-win64\\chromedriver.exe'
service = ChromeService(chrome_driver_path)
# Set up the Chrome WebDriver
driver = webdriver.Chrome(service=service, options=options)

# URL of the LinkedIn job search results page
target_url = 'https://www.linkedin.com/jobs/search/?currentJobId=3798762878&geoId=105080838&keywords=data%20engineer&location=New%20York%2C%20%C3%89tats-Unis&origin=JOB_SEARCH_PAGE_LOCATION_AUTOCOMPLETE&refresh=true&start={}'

# Open the initial URL to trigger JavaScript rendering
driver.get(target_url.format(0))
time.sleep(5)  # Allow time for the page to load dynamically

# Get the page source after JavaScript rendering
page_source = driver.page_source

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

# Extract the number of results
results_div = soup.find('div', class_='jobs-search-results-list__subtitle')
print(f"Number of Results: {results_div}")
if results_div:
    numeric_results = ''.join(c for c in results_div.find('span').get_text(strip=True) if c.isdigit())
    print(f"Number of Results: {numeric_results}")
else:
    print("Unable to extract the number of results.")



# Continue with your scraping logic...
l = []

for i in range(0, math.ceil(int(numeric_results) / 25)):
    driver.get(target_url.format(i))
    time.sleep(5)  # Allow time for the page to load dynamically
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    alljobs_on_this_page = soup.find_all("li")
    print(len(alljobs_on_this_page))
    for x in range(0, len(alljobs_on_this_page)):
        jobid = alljobs_on_this_page[x].find("div", {"class": "base-card"}).get('data-entity-urn').split(":")[3]
        l.append(jobid)

target_url = 'https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{}'
k = []

for j in range(0, len(l)):
    driver.get(target_url.format(l[j]))
    time.sleep(5)  # Allow time for the page to load dynamically
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    o = {}
    try:
        o["company"] = soup.find("div", {"class": "top-card-layout__card"}).find("a").find("img").get('alt')
    except:
        o["company"] = None

    try:
        o["job-title"] = soup.find("div", {"class": "top-card-layout__entity-info"}).find("a").text.strip()
    except:
        o["job-title"] = None

    try:
        o["level"] = soup.find("ul", {"class": "description__job-criteria-list"}).find("li").text.replace(
            "Seniority level", "").strip()
    except:
        o["level"] = None

    k.append(o)

df = pd.DataFrame(k)
df.to_csv('linkedinjobs.csv', index=False, encoding='utf-8')
print(k)

# Close the WebDriver
driver.quit()