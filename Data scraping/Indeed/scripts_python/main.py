from playwright.async_api import async_playwright
import asyncio
import re
import logging
from pathlib import Path
import json
import aiofiles
import sys

######################## CONSTANTS ########################

JOB_INFORMATIONS_SELECTORS = {
    "job_title": ".jobsearch-JobInfoHeader-title",
    "company": '[data-company-name="true"]',
    "job_location": '[data-testid="inlineHeader-companyLocation"]',
    "zip_code": '[data-testid="inlineHeader-companyLocation"]',
    "contract_element": ".js-match-insights-provider-h05mm8.e37uo190",
    "remote": '[data-testid="jobsearch-CompanyInfoContainer"]',
}
COMPANY_INFORMATIONS_SELECTORS = {
    "company_size": '[data-testid="companyInfo-employee"]',
    "company_turnover": '[data-testid="companyInfo-revenue"]',
    "company_industry": '[data-testid="companyInfo-industry"]',
}
SKILLS_DICT = {
    "ProgLanguage": [
        "Python",
        "Java",
        "C++",
        "C#",
        "Scala",
        " R,",
        "/R/",
        " R ",
        "Julia",
        "Kotlin",
        "Bash",
    ],
    "DataBase": [
        "SQL",
        "NoSQL",
        "MongoDB",
        "Cassandra",
        "Neo4j",
        "HBase",
        "Elasticsearch",
    ],
    "Data Analytics": ["Pandas", "NumPy", " R,", "/R/", " R ", "MATLAB"],
    "BigData": ["Hadoop", "Spark", "Databricks", "Flink", "Apache Airflow"],
    "MachineLearning": [
        "Scikit-Learn",
        "TensorFlow",
        "Keras",
        "PyTorch",
        "XGBoost",
        "LightGBM",
        "CatBoost",
        "Orange",
    ],
    "DataSerialization": [
        "Avro",
        "Protocol Buffers",
        "Json",
        "XML",
    ],
    "DataVisualisation": [
        "Tableau",
        "Power BI",
        "Matplotlib",
        "Seaborn",
        "Plotly",
    ],
    "Statistics": [
        "Statistiques Descriptives",
        "Inférentielles",
        "Bayesian Statistics",
        "Statistiques Bayésiennes",
    ],
    "CloudComputing": [
        "AWS",
        "Azure",
        "Google Cloud Platform",
        "GCP",
        "IBM Cloud",
        "Alibaba Cloud",
    ],
    "DevTools": ["Git", "Docker", "Jenkins", "Travis CI"],
    "OS": ["Linux", "Windows", "MacOS"],
    "DBMS": [
        "MySQL",
        "PostgreSQL",
        "Oracle SQL",
        "SQL Server",
        "Snowflake",
        "BigQuery",
        "Big Query",
        "SingleStore",
    ],
    "SoftBigDataProcessing": ["Apache Kafka", "Apache Flink", "HBase", "Cassandra"],
    "Automation": [
        "Ansible",
        "Kubernetes",
        "Puppet",
        "Chef",
        "Airflow",
    ],
    "InfrastructureAsCode": ["Terraform", "CloudFormation"],
    "NetworkSecurty": ["VPN", "Firewall", "SSL/TLS", "Wireshark"],
    "Virtualisation": ["VMware", "VirtualBox", "Hyper-V"],
    "Containers": ["Docker", "Kubernetes", "OpenShift"],
    "Collaboration": [
        "JIRA",
        "Confluence",
        "Slack",
        "Microsoft Teams",
        "Teams",
        "Discord",
    ],
    "Other": [
        "DevOps",
        "Backend Development",
        "Big Data",
        "ML",
        "Machine Learning",
        "Statistiques",
        "Cloud",
        "CI/CD",
        "CI / CD",
    ],
    "EnSoftSkils": [
        "Communication", "Teamwork", "Time Management", "Adaptability", "Problem Solving", "Leadership", "Creativity",
        "Empathy", "Collaboration", "Stress Management", "Organization", "Flexibility", "Initiative",
        "Critical Thinking", "Interpersonal Skills"
    ],
}
JOB_DESCRIPTION_SELECTOR = '[id="jobDescriptionText"]'


logging.basicConfig(
    level=logging.DEBUG,
    handlers=[
        logging.StreamHandler(stream=sys.stdout),
        logging.FileHandler("logfile.txt"),
    ],
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger()
logger.handlers[0].setLevel(logging.INFO)


async def handle_location(element):
    try:
        location_match = re.sub(r"\b\d+(?![a-zA-Z])", "", element)
        location = location_match.replace("(", "").replace(")", "").strip()

        zip_code_match = re.search(r"\b\d{3,}\b", element)
        zip_code = zip_code_match.group() if zip_code_match else None

        return {"location": location, "zip_code": zip_code}

    except Exception as e:
        logging.error(f"Error handling location or zip code: {str(e)}")
        return {"location": None, "zip_code": None}


async def get_remote(page, selector):
    try:
        elements = await page.query_selector_all(selector)

        for element in elements:
            value = await element.inner_text()

            if "télétravail" in value.lower():
                remote_value = re.search(r".*télétravail.*", value, re.IGNORECASE)
                return "remote", remote_value.group() if remote_value else None

        return "remote", None

    except Exception as e:
        logging.error(f"Error processing selector '{selector}': {str(e)}")
        return None


async def get_company_info(page, company_link, database):
    try:
        await page.goto(company_link)
        await page.wait_for_load_state("networkidle")

        for key, selector in COMPANY_INFORMATIONS_SELECTORS.items():
            try:
                element = await page.query_selector(selector)
                value = await element.inner_text() if element else None

                if value is not None:
                    # Nettoyer la valeur en remplaçant les motifs spécifiés
                    patterns_to_remove = [
                        "Taille de l'entreprise",
                        "Chiffre d'affaires",
                        "Secteur",
                        "Siège social",
                    ]
                    for pattern in patterns_to_remove:
                        value = (
                            value.replace(pattern, "")
                            .replace("\n", " ")
                            .replace("\xa0", " ")
                            .strip()
                        )

                else:
                    database[key] = None

                database[key] = value

            except Exception as e:
                logging.error(
                    f"Error processing company information '{selector}' for key '{key}': {str(e)}"
                )
        return database
    except Exception as e:
        logging.error(
            f"Error processing company information for link '{company_link}': {str(e)}"
        )
        return database


async def get_contract_infos(page, selector):
    try:
        elements = await page.query_selector_all(selector)
        salary_value, contract_type_value = None, None

        for element in elements:
            text = await element.inner_text()
            matches = re.findall(r"(\d+\s?\d+)(?: €)?", text, re.IGNORECASE)

            if len(matches) == 1:
                salary_value = matches[0]
            elif len(matches) == 2:  # Handle range with "De" before values
                salary_value = f"De {matches[0]} à {matches[1]}"

            contract_type_value = [
                word.strip()
                for word in text.lower().split()
                if word.strip()
                in [
                    "cdi",
                    "stage",
                    "freelance",
                    "cdd",
                    "interim",
                    "apprentissage",
                    "contrat pro",
                    "temps partiel",
                ]
            ]

        contract_type_value = contract_type_value[0] if contract_type_value else None

        return "salary", salary_value, "contract_type", contract_type_value

    except Exception as e:
        logging.error(f"Error processing selector '{selector}': {str(e)}")
        return None


async def get_company_link(page):
    try:
        links = await page.query_selector_all("a")

        await asyncio.sleep(0.5)

        company_link = await page.evaluate(
            r"(links) => {"
            + r"    const regex = /^https:\/\/fr\.indeed\.com\/cmp\/[^?]+/;"
            + r"    const filteredLinks = Array.from(links, link => link.href).filter("
            + r"        href => regex.test(href) && href.includes('?campaignid=mobvjcmp&from=mobviewjob')"
            + r"    );"
            + r"    return filteredLinks;"
            + r"}",
            links,
        )

    except Exception as e:
        logging.error(f"Error extracting links: {e}")
        raise

    return company_link[0] if company_link else None


def remove_url_from_file(file_path, url):
    with open(file_path, "r") as file:
        lines = file.readlines()

    with open(file_path, "w") as file:
        for line in lines:
            if line.strip() != url:
                file.write(line)


async def get_informations(url, page, job_informations_selectors):
    try:
        await page.goto(url)
        await page.wait_for_load_state("networkidle")

        job_info = {}

        for key, selector in job_informations_selectors.items():
            if key == "contract_element":
                result = await get_contract_infos(page, selector)
                job_info[result[0]] = result[1] if result else None
                job_info[result[2]] = result[3] if result else None
            elif key == "remote":
                result = await get_remote(page, selector)
                job_info[result[0]] = result[1] if result else None
            else:
                element = await page.query_selector(selector)
                value = await element.inner_text() if element else None

                if value is not None:
                    if key == "job_location" or key == "zip_code":
                        location_data = await handle_location(value)
                        job_info["job_location"] = location_data["location"]
                        job_info["zip_code"] = location_data["zip_code"]
                    else:
                        job_info[key] = value
                else:
                    job_info[key] = None

        return job_info

    except Exception as e:
        logging.error(f"Error processing URL '{url}': {str(e)}")
        return None
    await asyncio.sleep(0.5)


async def get_skills(page, selector, dictionary, database):
    element = await page.query_selector(selector)
    element_text = await element.inner_text() if element else None

    if element_text is not None:
        database["raw_description"] = element_text
        for key, values in dictionary.items():
            extracted_words = [
                word for word in values if word.lower() in element_text.lower()
            ]
            database[key] = extracted_words if extracted_words else None

    return database


file_lock = asyncio.Lock()


async def scrape_and_save(url, page, job_links_path, json_path):
    await page.goto(url)
    await page.wait_for_load_state("networkidle")
    await asyncio.sleep(0.5)

    job_info = await get_informations(url, page, JOB_INFORMATIONS_SELECTORS)
    job_info = await get_skills(page, JOB_DESCRIPTION_SELECTOR, SKILLS_DICT, job_info)

    company_link = await get_company_link(page)

    if company_link is not None:
        for attempt in range(2):
            try:
                job_info = await get_company_info(page, company_link, job_info)
                break  # Si la deuxième tentative réussit, sortir de la boucle
            except Exception as e:
                logging.error(
                    f"Error processing company information for link '{company_link}': {str(e)}"
                )

    logging.info(f"Job done: All data extracted from link {url}")

    if job_info is None or all(v is None for v in job_info):
        logging.info("Scraping unsuccessful, the link is conserved.")
    else:
        # Ajouter les résultats directement dans le fichier JSON en mode append
        async with aiofiles.open(json_path, "a", encoding="utf-8") as file:
            await file.write(json.dumps(job_info, ensure_ascii=False, indent=4))
            await file.write(",\n")

        remove_url_from_file(job_links_path, url)

    await asyncio.sleep(0.5)


async def main_batched(urls_batch, job_links_path, json_path):
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True)
        context = await browser.new_context()

        pages = [await context.new_page() for _ in range(20)]

        tasks = [
            scrape_and_save(url.strip(), page, job_links_path, json_path)
            for url, page in zip(urls_batch, pages)
        ]

        await asyncio.gather(*tasks)

        await asyncio.gather(*[page.close() for page in pages])
        await browser.close()


async def main():
    directory = Path.joinpath(Path(__file__).resolve().parent, "data")
    file_name = "indeed_db_v5.json"
    json_path = Path.joinpath(directory, file_name)
    job_links_path = Path.joinpath(directory, "job_links.txt")

    while True:

        with open(job_links_path, "r") as file:
            all_urls = file.readlines()

        if not all_urls:
            break

        batch_size = 100

        while all_urls:
            urls_batch = all_urls[:batch_size]

            await main_batched(urls_batch, job_links_path, json_path)

            all_urls = all_urls[batch_size:]


if __name__ == "__main__":
    asyncio.run(main())
