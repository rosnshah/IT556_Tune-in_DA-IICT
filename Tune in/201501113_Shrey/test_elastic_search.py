import csv
from elasticsearch import Elasticsearch, helpers

es = Elasticsearch()

request_body = {
    "settings": {
        "number_of_shards": 5,
        "number_of_replicas": 1
    },

    'mappings': {
        'generation1': {
            'properties': {
                'pokemon_no': {'type': 'integer'},
                'name': {'type': 'text'},
                'type1': {'type': 'text'},
                'type2': {'type': 'text'},
                'total': {'type': 'integer'},
                'hp': {'type': 'integer'},
                'attack': {'type': 'integer'},
                'defense': {'type': 'integer'},
                'specialattack': {'type': 'integer'},
                'specialdefense': {'type': 'integer'},
                'speed': {'type': 'integer'},
                'stage': {'type': 'integer'},
                'legendary': {'type': 'text'}
            }}}
}

print("creating 'pokemon' index...")
es.indices.create(index='pokemon', body=request_body)

