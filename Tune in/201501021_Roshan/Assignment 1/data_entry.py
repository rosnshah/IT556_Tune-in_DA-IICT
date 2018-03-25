import csv
from elasticsearch import Elasticsearch, helpers

es = Elasticsearch()

with open('Pokemon.csv', 'rU') as f:
    reader = csv.DictReader(f)
    helpers.bulk(es, reader, index='pokemon', doc_type='generation1')