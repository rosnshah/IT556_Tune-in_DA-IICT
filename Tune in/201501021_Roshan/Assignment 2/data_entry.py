import json
from elasticsearch import Elasticsearch, helpers

es = Elasticsearch()

data = json.loads(open("./musicdataset.json", encoding="utf8").read())

i = 0

while i < 500:
    es.index(index='music_data', doc_type='music', id=i, body=data[i])
    i += 1

print("Data inserted with mapping......")