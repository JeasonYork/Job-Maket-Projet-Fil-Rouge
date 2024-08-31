#!/bin/bash

curl -X GET "http://localhost:9200/jobmarket/_search" -H 'Content-Type: application/json' -d'
{
  "size": 0,
  "aggs": {
    "sources": {
      "terms": {
        "field": "source.keyword",
        "size": 5
      }
    }
  }
}'
