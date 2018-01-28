import json
import requests
from elasticsearch import Elasticsearch
from collections import namedtuple

es = Elasticsearch([{
    'host': 'localhost',
    'port': 9200
}])

request_body = {
    "mappings": {
        "music": {
            "properties": {
				'id': {'type': 'integer'},
                'Year': {'type': 'integer'},
                'Album': {'type': 'text'},
                'Artist': {'type': 'text'},
                'Genre': {'type': 'text'},
                'Subgenre': {'type': 'text'}

            }
        }
    },

    "settings": {
        "number_of_shards": 5,
        "number_of_replicas": 1
    }
}

es.indices.create(index='music_data', body=request_body)