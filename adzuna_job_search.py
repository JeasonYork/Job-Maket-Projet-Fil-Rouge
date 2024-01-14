# adzuna_job_search.py

import requests
import json
import csv

base_url = "http://api.adzuna.com/v1/api/jobs/gb/search/1"
api_key = "893a665a637d864b72c8d5a31999ff5c"

params = {
    "app_id": "31039764",
    "app_key": api_key,
    "results_per_page": 1000,
    "what": "data engineer",
    "content-type": "application/json",
    "where": "france",
}

response = requests.get(base_url, params=params)
data = response.json()

# Handle and process the data as needed
print(data)

# Save the data into a JSON file
with open("adzuna_job_market.json", "w") as json_file:
    json.dump(data, json_file)

print("Data saved to adzuna_job_market.json")

# Save the data into a CSV file
csv_filename = "adzuna_job_market.csv"

# Extract relevant information from the JSON data
job_listings = data.get("results", [])

# Save to CSV
with open(csv_filename, "w", newline="", encoding="utf-8") as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=["title", "company", "location"])
    
    csv_writer.writeheader()
    
    # Write data
    for job in job_listings:
        csv_writer.writerow({
            "title": job.get("title", ""),
            "company": job.get("company", {}).get("display_name", ""),
            "location": job.get("location", {}).get("display_name", "")
        })

print(f"Data saved to {csv_filename}")