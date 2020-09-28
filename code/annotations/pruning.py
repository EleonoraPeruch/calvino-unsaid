#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import spacy
import it_core_news_sm
import requests
import pprint
from rdflib import Graph, URIRef
import sys
#from tagme import dict_tagme

nlp = spacy.load("it_core_news_sm")

sample_file = "C:/Users/us/Desktop/DHDK/a.a.2019-2020/Tesi/extraction/spacy/leggerezza_trial.txt"
with open(sample_file, "r", encoding="latin1") as f:
    text = f.read()
    #print(text)

doc = nlp(text)
named_entity_dict = {}

#ents = [(e.text, e.start_char, e.end_char, e.label_) for e in doc.ents]
#print(ents)
entity_list = []
list = []

for e in doc.ents:
    list.append(e.start_char)
    list.append(e.end_char)
    #named_entity_dict[e] = tuple()
    named_entity_dict[str(e)] = tuple(list)
    list = []
#print(named_entity_dict)

tagme_data = "C:/Users/us/Desktop/DHDK/a.a.2019-2020/Tesi/extraction/spacy/tagme_data.json"
with open(tagme_data, "r", encoding="latin1") as t:
    #t = sys.stdin.buffer.read(16).decode(sys.stdin.encoding)
    json_obj = json.load(t)
    t.close()

#tagme_data = "C:/Users/us/Desktop/DHDK/a.a.2019-2020/Tesi/extraction/spacy/tagme_data.json"
#with open(tagme_data, "r", encoding="latin1") as t:
#    json_obj = json.load(t)
#    t.close()


for k, v in json_obj.items():
    for dict in json_obj[k]:
        for dict_min in dict["annotations"]:
            for key, value in named_entity_dict.items():
                if key in dict_min["title"]:
                    #print(dict_min["title"])
                    #print(key)
                    #print(int(dict_min["end"] - dict_min["start"]))
                    #print(int(named_entity_dict[key][1] - named_entity_dict[key][0]))
                    if int(dict_min["end"] - dict_min["start"]) == int(named_entity_dict[key][1] - named_entity_dict[key][0]) and dict_min["title"] not in entity_list:
                         entity_list.append(dict_min["title"])
                #else:
                #    entity_list.append(key)
print(named_entity_dict)
print(entity_list)

#for i in dict_tagme["leggerezza_tagme"]:
#    for e in i["annotations"]:
#        for key in named_entity_dict.keys():
#            if key == e["title"]:
        #if e["title"] == key for key in named_entity_dict.keys():
#                if (int(e["end"]) - int(e["start"])) == (int(named_entity_dict[key][1]) - int(named_entity_dict[key][0])):
#                    print(named_entity_dict[key])


#for i in dict_tagme["leggerezza_tagme"]:
#    for e in i["annotations"]:
#        if #start in spacy named entity == e["start"] and end in spacy named entity == e["end"]:
            #correct, select the entity
        #else:
            #discard the entity, not relevant
