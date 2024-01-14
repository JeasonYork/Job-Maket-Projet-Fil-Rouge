# Import Packages
from selenium import webdriver
import time
import pandas as pd
import os

# Import additional packages
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service


# Specify the path to the chromedriver executable
chrome_driver_path = r'C:\\Users\\Default\\Desktop\\chromedriver-win64\\chromedriver.exe'

# Create a Chrome Service instance
chrome_service = Service(chrome_driver_path)

# Create a Chrome WebDriver instance using the service
driver = webdriver.Chrome(service=chrome_service)

# Rest of your code
driver.implicitly_wait(20)
url1 = 'https://www.linkedin.com/jobs/search/?currentJobId=3776009950&geoId=105015875&keywords=data%20engineer&location=France&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true'
driver.get(url1)

# Find number of job listings using a more generic approach
job_count_element = driver.find_element(By.CLASS_NAME, 'results-context-header__job-count')
y = job_count_element.text if job_count_element else 'Not Found'

print(type(y))

# Try to convert to numeric, and handle errors
try:
    n = pd.to_numeric(y, errors='coerce')
    print(n)
except ValueError:
    print("Unable to convert to numeric.")

#Loop to scroll through all jobs and click on see more jobs button for infinite scrolling

i = 2
while i <= int((n+200)/25)+1: 
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    i = i + 1
    
    try:
        send=driver.find_element_by_xpath("//button[@aria-label='Load more results']")
        driver.execute_script("arguments[0].click();", send)   
        time.sleep(3)
    
        
         #buu=driver.find_elements_by_tag_name("button")
         #x=[btn for btn in buu if btn.text=="See more jobs"]
         #for btn in x:
                #driver.execute_script("arguments[0].click();", btn)
                #time.sleep(3)
  
    except:
        pass
        time.sleep(5)

#Create empty lists for company name and job title

companyname= []
titlename= []

#Find company name and append it to the blank list

try:
    for i in range(n):
        company=driver.find_elements_by_class_name('base-search-card__subtitle')[i].text
        companyname.append(company)
         
except IndexError:
    print("no")
        
    
  #Find title name and append it to the blank list

try:
    for i in range(n):
        
        
        title=driver.find_elements_by_class_name('base-search-card__title')[i].text
    

        titlename.append(title)
        
  
except IndexError:
    print("no")

#Create dataframe for company name and title

companyfinal=pd.DataFrame(companyname,columns=["company"])
titlefinal=pd.DataFrame(titlename,columns=["title"])

#Join the two lists

x=companyfinal.join(titlefinal)

#Save file in your directory

x.to_csv('linkedin.csv')


#Find job links and append it to a list

jobList = driver.find_elements_by_class_name('base-card__full-link')
hrefList = []
for e in jobList:
    hrefList.append(e.get_attribute('href'))

#for href in hrefList:
    #link.append(href)