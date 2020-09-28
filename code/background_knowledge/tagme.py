# -*- coding: utf-8 -*-
#import sparql
import json
import spacy
import it_core_news_sm
import requests
#from rdflib import Graph, URIRef, plugin
#import pprint
#import time
#from joint import corpus
#from tagme_categories import hist_cat, cross_cat, cogn_cat, inter_cat

# tagme token
# 45be3d7d-dc87-4d02-b8fb-5de722a99379-843339462

nlp = spacy.load("it_core_news_sm")
sample_file = "C:/Users/us/Desktop/DHDK/a.a.2019-2020/Tesi/extraction/spacy/la_leggerezza.txt"
data_tag = open("C:/Users/us/Desktop/DHDK/a.a.2019-2020/Tesi/extraction/spacy/data_tag.txt", "w", encoding="utf8")

with open(sample_file, "r", encoding="utf-8") as f:
    text = f.read()

doc = nlp(text)
dict_tagme = {}
list = []

# sentence segmentation
for sent in doc.sents:
    #print(sent.text)
    r = requests.get("https://tagme.d4science.org/tagme/tag?lang=it&include_abstract=false&include_categories=true&gcube-token=45be3d7d-dc87-4d02-b8fb-5de722a99379-843339462&text="+sent.text)
    data_tag.write(r.text)
    data_tag.write(",")
    file = json.loads(r.text) # parse a json string with loads
    list.append(file)

dict_tagme = {"leggerezza_tagme": list }
#print(dict_tagme)
#print(json.dumps(dict_tagme, indent=4))

with open("tagme_data.json", "w", encoding="utf8") as output:
    json.dump(dict_tagme, output, indent=4, ensure_ascii=False) # convert a Python object into a json script with dump

#tagme = "C:/Users/us/Desktop/DHDK/a.a.2019-2020/Tesi/extraction/spacy/tagme_data.json"
#with open(tagme, "r", encoding="utf-8") as t:
#    json = t.read()
#g = Graph()
#g.parse(data=json, format="json")
#print(g.serialize(format='turtle'))

#-------------------------------------------------------------------------
#for i in dict_tagme["leggerezza_tagme"][0]["annotations"]:
#    print (i["dbpedia_categories"])

#for i in dict_tagme["leggerezza_tagme"]:
#    for e in i["annotations"]:
#        for cat in e["dbpedia_categories"]:
        # if cat in ... for cat in e["dbpedia_categories"]
            #print(cat) e.g. Prima guerra mondiale
#            if cat in str(hist_cat):
#                print(e["spot"])
#            else:
#                print("not relevant")
#aggiungere lo spot al corpus per costruire il knowledge graph
