# MAin script to get jobs from Linkedin for our Data engineering project Jan 2014
# Import necessary packages for web scraping and logging
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
import pandas as pd
import random
import time
from time import sleep
import json
import re
import datetime

# Configure logging settings
logging.basicConfig(filename="scraping.log", level=logging.INFO)

skill_categories = {
        "ProgLanguage": ("Python", "Java", "C++", "C#", "Scala", "R", " R ", "/R/", "Julia", "Go", "Kotlin", "Bash", "JavaScript", "HTML"),
        "DataBase": ("SQL", "NoSQL", " MongoDB", "Cassandra", "Neo4j", "HBase", "Elasticsearch"),
        "DataAnalytics": ("Pandas", "NumPy", "R", " R ", "/R/", "MATLAB"),
        "BigData": ("Hadoop", "Spark", "Databricks", "Flink", "Apache Airflow"),
        "MachineLearning": ("Scikit-Learn", "TensorFlow", "Keras", "PyTorch", "XGBoost", "LightGBM", "CatBoost", "Orange"),
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
job_detail = {
        "JobDetail":("Hybride","Remote","Temps plein","Full","Confirmé","Confirmed","Junior","Senior"),
        "TypeContract":("CDI","CDD","Freelence"),
        "Salary":("Salaire","Salary","Rénumeration","Renumeration","Package"),
        "Level":("Bac+5","Bac+3"),
        "Experience":("ans"),
    }
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

def extract_job_details(description: str) -> dict:
    """
    Extract job details such as job type, contract type, salary, etc. from the description.

    Args:
        description (str): The job description text.

    Returns:
        dict: A dictionary containing extracted job details.
    """
    job_details = {category: [] for category in job_detail}

    try:
        # Iterate over each category in job_detail
        for category, details in job_detail.items():
            # Check if any detail in the category is mentioned in the description
            mentioned_details = [detail for detail in details if detail.lower() in description.lower()]

            # Append mentioned details to the corresponding category list in job_details
            job_details[category] = mentioned_details

        # Extract salary using regular expression
        salary_matches = []
        for keyword in job_detail["Salary"]:
            keyword_position = description.lower().find(keyword.lower())
            if keyword_position != -1:
                salary_match = re.search(r'\b\d+(?:[.,]\d+)?(?:\s?[Kk]|€|euros?)?\b', description[keyword_position+len(keyword):])
                if salary_match:
                    salary_matches.append(salary_match.group())
        if salary_matches:
            job_details["Salary"] = salary_matches

       # Extract experience using regular expression
        for keyword in job_detail["Experience"]:
            experience_match = re.search(r'\b(\d+)\s?ans\b', description, re.IGNORECASE)
            if experience_match:
                job_details["Experience"].append(experience_match.group(1))

    except Exception as e:
        logging.warning(f"An error occurred while extracting job details: {str(e)}")

    return job_details


def scrape_linkedin_jobs(job_title: str, location: str, pages: int = None) -> list:
    """
    Scrape job listings from LinkedIn based on job title and location.

    Parameters
    ----------
    job_title : str
        The job title to search for on LinkedIn.
    location : str
        The location to search for jobs in on LinkedIn.
    pages : int, optional
        The number of pages of job listings to scrape. If None, all available pages will be scraped.

    Returns
    -------
    list of dict
        A list of dictionaries, where each dictionary represents a job listing
        with the following keys: 'job_title', 'company_name', 'location', 'posted_date',
        and 'job_description'.
    """

    # Log a message indicating that we're starting a LinkedIn job search
    logging.info(f'Starting LinkedIn job scrape for "{job_title}" in "{location}"...')

           
    # Sets the pages to scrape if not provided
    pages = pages or 1

    # Set up ChromeOptions
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--log-level=2")  

    # Specify the path to your chromedriver executable
    chrome_driver_path = r'C:\\Users\\Default\\Desktop\\chromedriver-win64\\chromedriver.exe'
    service = ChromeService(chrome_driver_path)
    # Set up the Chrome WebDriver
    driver = webdriver.Chrome(service=service, options=options)
    """
    driver.get("https://www.linkedin.com/login")

    # Find the username and password input fields and enter your credentials
    username_field = driver.find_element_by_id("username")
    username_field.send_keys("csaid07@****")  

    password_field = driver.find_element_by_id("password")
    password_field.send_keys("****")  

    # Submit the form
    password_field.send_keys(Keys.RETURN)

    # Wait for the page to load
    time.sleep(5) 
    """
    # Navigate to the LinkedIn job search page with the given job title and location
    driver.get(
        f"https://www.linkedin.com/jobs/search/?keywords={job_title}&location={location}"
    )

    # Scroll through the first 50 pages of search results on LinkedIn
    for i in range(pages):

        # Log the current page number
        logging.info(f"Scrolling to bottom of page {i+1}...")

        # Scroll to the bottom of the page using JavaScript
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        try:
            # Wait for the "Show more" button to be present on the page
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[1]/div/main/section[2]/button")
                )
            )
            # Click on the "Show more" button
            element.click()

        # Handle any exception that may occur when locating or clicking on the button
        except Exception:
            # Log a message indicating that the button was not found and we're retrying
            logging.info("Show more button not found, retrying...")

        # Wait for a random amount of time before scrolling to the next page
        time.sleep(random.choice(list(range(3, 7))))

    # Scrape the job postings
    jobs = []
    soup = BeautifulSoup(driver.page_source, "html.parser")
    job_listings = soup.find_all(
        "div",
        class_="base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card",
    )

    try:
        for job in job_listings:
            # Extract job details

            # job title
            job_title = job.find("h3", class_="base-search-card__title").text.strip()
            # job company
            job_company = job.find(
                "h4", class_="base-search-card__subtitle"
            ).text.strip()
            # job location
            job_location = job.find(
                "span", class_="job-search-card__location"
            ).text.strip()
            # job link
            apply_link = job.find("a", class_="base-card__full-link")["href"]

            # Navigate to the job posting page and scrape the description
            driver.get(apply_link)

            # Sleeping randomly
            time.sleep(random.choice(list(range(5, 11))))

            # Use try-except block to handle exceptions when retrieving job description
            try:
                # Create a BeautifulSoup object from the webpage source
                description_soup = BeautifulSoup(driver.page_source, "html.parser")

                # Find the job description element and extract its text
                job_description = description_soup.find(
                "div", class_="description__text description__text--rich").get_text(strip=True, separator='\n')

                # Extract skills from the job description
                extracted_skills = extract_skills(job_description)

                # Extract job details using extract_job_details function
                job_details = extract_job_details(job_description)

            # Handle the AttributeError exception that may occur if the element is not found
            except AttributeError:
                # Assign None to the job_description variable to indicate that no description was found
                job_description = None

                # Write a warning message to the log file
                logging.warning(
                    "AttributeError occurred while retrieving job description."
                )

            # Add job details to the jobs list
            jobs.append(
                {
                    "source": "LinkedIn",
                    "title": job_title,
                    "company": job_company,
                    "location": job_location,
                    "link": apply_link,
                    "description": job_description,
                    "skills": extracted_skills,
                    "details": job_details,
                }
            )
            # Logging scrapped job with company and location information
            logging.info(f'Scraped "{job_title}" at {job_company} in {job_location}...')

    # Catching any exception that occurs in the scrapping process
    except Exception as e:
        # Log an error message with the exception details
        logging.error(f"An error occurred while scraping jobs: {str(e)}")

        # Return the jobs list that has been collected so far
        # This ensures that even if the scraping process is interrupted due to an error, we still have some data
        return jobs

    # Close the Selenium web driver
    driver.quit()

    # Return the jobs list
    return jobs


def save_job_data(data: dict, job_title: str, location: str, pages: int) -> None:
    """
    Save job data to a CSV file.

    Args:
        data: A dictionary containing job data.
        job_title: The job title used for the search.
        location: The location used for the search.
        pages: The number of pages scraped.

    Returns:
        None
    """

    # Format current date and time
    current_datetime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    # Format job title for file name
    formatted_job_title = job_title.replace(" ", "_")

    # Construct file names
    csv_file_name = f"Jobs_{formatted_job_title}_{current_datetime}_Pages{pages}.csv"
    json_file_name = f"Jobs_{formatted_job_title}_{current_datetime}_Pages{pages}.json"

    # Create a pandas DataFrame from the job data dictionary
    df = pd.DataFrame(data)

    # Save the DataFrame to a CSV file without including the index column
    df.to_csv(csv_file_name, index=False)

    # Save the data to a JSON file
    with open(json_file_name, "w") as json_file:
        json.dump(data, json_file, indent=4)

    # Log a message indicating how many jobs were successfully scraped and saved to the CSV file
    logging.info(f"Successfully scraped {len(data)} jobs and saved to {csv_file_name} and {json_file_name}")

# Call the functions below
job_title_list = [
    "data engineer",
    "data architect",
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
    "ETL Developer",
]

location = "France"
pages = 20

for position in job_title_list:

    data = scrape_linkedin_jobs(position, location, pages)
    save_job_data(data, position, location, pages)
