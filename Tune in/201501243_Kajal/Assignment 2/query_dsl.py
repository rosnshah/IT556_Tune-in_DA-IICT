import json
import requests
from elasticsearch import Elasticsearch
from collections import namedtuple

INDEX_NAME='music_data'

es = Elasticsearch([{
    'host': 'localhost',
    'port': 9200
}])


# 1.Boolean FOormation

#Query to display all the albums released till today by 'Bob Dylan'

res = es.search(index=INDEX_NAME, body={
    "query": {
    "bool": {
      "must":
        { "match": { "Artist": "Bob Dylan"}}
    }
  }
})
#print(" response: '%s'" % (res))

# Query to display all the albums with Genre as 'Hip Hop'

res = es.search(index=INDEX_NAME, body={

    "query": {
    "bool": {
      "must":
        { "match": { "Genre": "Hip Hop"}}
    }
  }
})
#print(" response: '%s'" % (res))


# Query to display albums by 'The Beatles' in the Genre 'Rock' , released after '1970'
res = es.search(index=INDEX_NAME, body={
    "query": {

        "bool": {
            "must": {
                "match": {"Genre": "Rock"}
            },
            "filter": {
                "match": {"Artist": "Beatles"}
            },
            "must_not": {
                "range": {
                    "Year": {"lte": 1970}
                }
            }
        }
    }
})
#print(" response: '%s'" % (res))








# 2.BOOSTING

res = es.search(index=INDEX_NAME, body={
    "query": {
        "boosting": {
            "positive": {
                "term": {
                    "Year": "2000"
                }
            },
            "negative": {
                "term": {
                    "Genre": "Hip Hop"
                }
            },
            "negative_boost": 0.6
        }

    }
})
#print(" response: '%s'" % (res))

#3. MIinimum_Should_Match

# Query to display with minimum_should_match as 1.
#Display results where artist is 'pink floyd' or genre is 'rock' or year of release is '1979'

res = es.search(index=INDEX_NAME, body={
    "query": {

        "bool": {

            "should": [
                {"match": {"Artist":"Pink Floyd"}},
                {"match": {"Genre": "Rock"}},
                {"match": {"Year": 1979}}
            ],
            "minimum_should_match": 1

        }
    }
})
#print(" response: '%s'" % (res))


#Query to display with minimum_should_match as 3.
#Display results where artist is 'pink floyd' and genre is 'rock' and year of release is '1979'

res = es.search(index=INDEX_NAME, body={
    "query": {

        "bool": {

            "should": [
                {"match": {"Artist":"Pink Floyd"}},
                {"match": {"Genre": "Rock"}},
                {"match": {"Year": 1979}}
            ],
            "minimum_should_match": 3

        }
    }
})
#print(" response: '%s'" % (res))

#Query to display all albums of genre 'Rock' in the year '1983' using minimun_should_match

res = es.search(index=INDEX_NAME, body={
    "query": {

        "bool": {

            "should": [
                {"match": {"Genre": "Rock"}},
                {"match": {"Year": 1983}}
            ],
            "minimum_should_match": 2

        }
    }
})
#print(" response: '%s'" % (res))