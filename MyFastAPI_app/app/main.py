from fastapi import FastAPI, HTTPException, Security, Depends
from typing import List, Optional
from pydantic import BaseModel
from .elastic import get_es_client
import base64
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from .config import admins, hash_password, verify_password

app = FastAPI(
    title="Job Market API",
    description="Job Market API powered by FastAPI.",
    version="1.0.1")

# utilisateurs voir config.py

# Fonction d'authentification admin
def authenticate_admin(credentials: HTTPBasicCredentials = Depends(HTTPBasic())):
    username = credentials.username
    password = credentials.password
    if username in admins and verify_password(password, admins[username]):
        return username
    else:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Basic"},
        )


# Obtenir le client Elasticsearch
es = get_es_client()

# Modèle de données pour les offres d'emplois
class JobOffer(BaseModel):
    id: Optional[str]
    source: str
    title: str
    company: str
    location: str
    link: str
    description: str
    skills: dict
    details: dict

@app.get("/")
def read_root():
    """ Main root API for test """
    return {"Hello": "World"}

# Endpoint pour récupérer les offres d'emplois
@app.get("/job_offers/", response_model=List[JobOffer])
async def get_job_offers(query: Optional[str] = None):
    """Obtenir la liste des Jobs selons les critères
       - Si query est fourni, il est divisé en mots-clés individuels à l'aide de split().
       - Si La query contient plusieur mots clés (Data engineer, spark, python, Azure),
         Chaque multi_match recherche dans les champs spécifiés (title, description, company) 
         pour le mot-clé correspondant. Exemple http://localhost:8000/job_offers/?query=data%20engineer.
       - Si le champ query est vide, 10000 offres seront retourné de l'indice jobmarket
    """
    try:
        if query:
            # Split des mots-clés pour construire une recherche avec plusieurs termes
            keywords = query.split()
            # Construction de la requête Elasticsearch
            query_body = {
                "query": {
                    "bool": {
                        "should": [
                            {"multi_match": {
                                "query": keyword,
                                "fields": ["title", "description", "company"]
                            }} for keyword in keywords
                        ]
                    }
                }
            }
            result = es.search(index="jobmarket", body=query_body)
        else:
            # Requête Elasticsearch pour obtenir toutes les offres d'emplois
            query_body = {
                "query": {
                    "match_all": {}
                },
                "size": 10000  # Pour récupérer jusqu'à 10000 documents
            }
            result = es.search(index="jobmarket", body=query_body)

        # Récupération des résultats de la recherche
        hits = result["hits"]["hits"]
        job_offers = [
            JobOffer(id=hit["_id"], **hit["_source"]) for hit in hits
        ]
        return job_offers

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint pour créer une nouvelle offre d'emploi
@app.post("/job_offers/", response_model=JobOffer)
async def create_job_offer(job_offer: JobOffer, username: str = Security(authenticate_admin)):
    """Créer une nouvelle offre d'emploi
       - La méthode create_job_offer prend un objet JobOffer en corps de la requête et l'indexe dans Elasticsearch.
       - Retourne l'offre d'emploi nouvellement créée avec son ID.
    """
    try:
        result = es.index(index="jobmarket", document=job_offer.dict())
        job_offer_id = result['_id']
        return {**job_offer.dict(), "id": job_offer_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint pour supprimer une offre d'emploi par ID
@app.delete("/job_offers/{job_id}")
async def delete_job_offer(job_id: str, username: str = Security(authenticate_admin)):
    """Supprimer une offre d'emploi en fonction de son ID"""
    try:
        result = es.delete(index="jobmarket", id=job_id)
        if result['result'] == 'deleted':
            return {"message": "Job offer deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Job offer not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint pour modifier une offre d'emploi par ID
@app.put("/job_offers/{job_id}")
async def update_job_offer(job_id: str, job_offer: JobOffer, username: str = Security(authenticate_admin)):
    """Mettre à jour une offre d'emploi en fonction du job_id"""
    try:
        result = es.update(index="jobmarket", id=job_id, body={"doc": job_offer.dict()})
        if result['result'] == 'updated':
            return {"message": "Job offer updated successfully"}
        else:
            raise HTTPException(status_code=404, detail="Job offer not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


