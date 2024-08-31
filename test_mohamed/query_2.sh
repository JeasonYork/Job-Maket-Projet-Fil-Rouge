#!/bin/bash

# Effectuer une recherche pour obtenir un document aléatoire
response=$(curl -s -X GET "http://localhost:9200/jobmarket/_search" -H 'Content-Type: application/json' -d'
{
  "query": {
    "function_score": {
      "functions": [
        {
          "random_score": {}
        }
      ]
    }
  },
  "size": 1
}')

# Imprimer le document aléatoire
echo "Document aléatoire :"
echo $response
