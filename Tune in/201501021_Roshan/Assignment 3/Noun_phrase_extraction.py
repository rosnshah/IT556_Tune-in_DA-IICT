# Team Tune In
# Noun phrase extraction from item description
import spacy
import json
nlp = spacy.load('en')
dataset = open("Billboard_2014.json",encoding="utf8")
data = json.load(dataset)
#We will be extracting noun phrase from Lyrics since it will have maximum cases of sentences
for i in range(1,11):
    print(i)
    doc = nlp(data[i-1]['Lyrics'])
    for np in doc.noun_chunks:
        print("Text: ",np.text)
        print("Root Text: ",np.root.text)
        print("Dependency: ",np.root.dep_)
        print("Root Head Text: ", np.root.head.text)
        print()
