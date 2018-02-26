# Team Tune In
# Lemmatization of verb phrases
import spacy
import json
nlp = spacy.load('en')
dataset = open("Billboard_2014.json",encoding="utf8")
data = json.load(dataset)
#We will be lemmatizing verbs from Lyrics since it will have maximum cases of it
for i in range (1,11):
    print(i)
    doc = nlp(data[i-1]['Lyrics'])
    for token in doc:
        if token.pos_ == "VERB": # If the token is verb then give its base form
            print("Verb: ",token.text,", Base form: ",token.lemma_)
