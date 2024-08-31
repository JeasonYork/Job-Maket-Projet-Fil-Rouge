#!/bin/bash

curl -X POST "http://localhost:9200/jobmarket/_delete_by_query" -H 'Content-Type: application/json' -d'
{
  "query": {
    "bool": {
      "should": [
        { "term": { "source.keyword": "Indeed" } },
        { "term": { "source.keyword": "welcometothejungle" } }
      ]
    }
  }
}'
