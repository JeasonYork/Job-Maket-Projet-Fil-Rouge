import requests
import json
from requests.auth import HTTPBasicAuth

# URL de base de l'API
base_url = "http://localhost:8000"

# Authentification de base
auth = HTTPBasicAuth('admin', '@dmin7')

# Fonction pour lire la racine
def read_root():
    print("""
============================
          root Test
============================""")
    try:
        response = requests.get(f"{base_url}/")
        print(response.request.method, response.request.url)
        response.raise_for_status()
        print("GET / Read Root:")
        print(response.json())
        print("\n ==> SUCCES")
    except requests.exceptions.RequestException as e:
        print(f"Error during GET / request: {e}")
        print("FAILURE")
    #print("\n")

# Fonction pour obtenir des offres d'emploi
def get_job_offers(query):
    print("""
============================
    GET /job_offers/ Test
============================""")
    try:
        response = requests.get(f"{base_url}/job_offers/", params={"query": query})
        print(response.request.method, response.request.url)
        response.raise_for_status()
        job_offers = response.json()
        if isinstance(job_offers, list):
            for job in job_offers:
                print(f"ID: {job.get('id')}, Source:{job.get('souce')}, Title: {job.get('title')}, Company: {job.get('company')}")
        print("\n ==> SUCCES")
    except requests.exceptions.RequestException as e:
        print(f"Error during GET /job_offers/ request: {e}")
        print("FAILURE")
    #print("\n")

# Fonction pour créer une offre d'emploi
def create_job_offer(job_offer):
    print("""
============================
    POST /job_offers/ Test
============================""")
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(f"{base_url}/job_offers/", data=json.dumps(job_offer), headers=headers, auth=auth)
        print(response.request.method, response.request.url)
        response.raise_for_status()
        print("POST /job_offers/ Create Job Offer:")
        job_offer_response = response.json()
        print(job_offer_response)
        print("\n ==> SUCCES")
        #print("\n")

        # Retourner l'ID de l'offre d'emploi créée
        if 'id' in job_offer_response:
            job_id = job_offer_response['id']
            return job_id
    except requests.exceptions.RequestException as e:
        print(f"Error during POST /job_offers/ request: {e}")
        print("FAILURE")
        print("\n")
        return None

# Fonction pour supprimer une offre d'emploi
def delete_job_offer(job_id):
    print("""
============================
    DELETE /job_offers/ Test
============================""")
    try:
        response = requests.delete(f"{base_url}/job_offers/{job_id}", auth=auth)
        response.raise_for_status()
        print(f"DELETE /job_offers/{job_id} Delete Job Offer:")
        print(response.json())
        print("\n ==> SUCCES")
    except requests.exceptions.RequestException as e:
        print(f"Error during DELETE /job_offers/{job_id} request: {e}")
        print("FAILURE")
    #print("\n")

# Fonction pour mettre à jour une offre d'emploi
def update_job_offer(job_id, job_offer):
    print("""
============================
    PUT /job_offers/ Test
============================""")
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.put(f"{base_url}/job_offers/{job_id}", data=json.dumps(job_offer), headers=headers, auth=auth)
        print(response.request.method, response.request.url)
        response.raise_for_status()
        print(f"PUT /job_offers/{job_id} Update Job Offer:")
        print(response.json())
        print("\n ==> SUCCES")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Print HTTP error message
        if response.status_code == 422:
            print(f"Response content: {response.content}")  # Print response content for debugging
        print("FAILURE")
    except requests.exceptions.RequestException as e:
        print(f"Error during PUT /job_offers/{job_id} request: {e}")
        print("FAILURE")
    #print("\n")


if __name__ == "__main__":
    # Lire la racine
    read_root()

    # Obtenir des offres d'emploi avec une query
    get_job_offers("Data engineer, Azure")

    # Créer une nouvelle offre d'emploi
    new_job_offer = {
        "id": "",
        "source": "TestAPI",
        "title": "Example Engineer",
        "company": "Example Company",
        "location": "Example Location",
        "link": "http://example.com",
        "description": "Example job description",
        "skills": {},
        "details": {"experience": "ExampleExperience"}
    }

    updated_job_offer = {
        "id": "1",
        "source": "updated_source",
        "title": "Senior Data Engineer",
        "company": "Updated Company",
        "location": "Updated Location",
        "link": "http://updated.com",
        "description": "Updated job description",
        "skills": {},
        "details": {"experience": "Updated Experience"}
    }

    job_id = create_job_offer(new_job_offer)

    # Supprimer l'offre d'emploi créée
    if job_id:
        update_job_offer(job_id, updated_job_offer)
        delete_job_offer(job_id)
    else:
        print("No job_id")
