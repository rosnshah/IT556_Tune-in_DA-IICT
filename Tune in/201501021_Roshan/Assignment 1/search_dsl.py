
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
es = Elasticsearch()
print(es.search(index="pokemon", body={"query": {"match": {'name':'Pidgey'}}}))