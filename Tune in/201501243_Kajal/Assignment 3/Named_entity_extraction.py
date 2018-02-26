# Team Tune In
# Named Entity extraction and recognition in item descriptionNamed Entity extraction and recognition in item description
import spacy
import json
nlp = spacy.load('en')
dataset = open("Billboard_2014.json",encoding="utf8")
data = json.load(dataset)

for i in range (1,11):
    print(i)
    doc = nlp(data[i-1]['Lyrics'])
    for ent in doc.ents:
        print("Text: ",ent.text,"Label:",ent.label_)