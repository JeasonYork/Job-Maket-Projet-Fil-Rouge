#!/bin/bash

curl -X GET "http://localhost:9200/jobmarket/_search" -H 'Content-Type: application/json' -d'

{
  "size": 0,
  "aggs": {
    "locations": {
      "terms": {
        "field": "location.keyword", 
        "size": 10000
      }
    }
  }
}'
