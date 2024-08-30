import subprocess

command = '''
curl -X POST "http://localhost:9200/jobmarket/_delete_by_query" -H 'Content-Type: application/json' -d'
{
  "query": {
    "match_all": {}
  }
}'
'''

subprocess.run(command, shell=True, check=True)
