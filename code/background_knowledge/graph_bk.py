# -*- coding: utf-8 -*-
import sparql
from SPARQLWrapper import SPARQLWrapper, TURTLE
import json
import spacy
import it_core_news_sm
import requests
import pprint
from rdflib import Graph, URIRef
import pprint
from pruning import entity_list

#--------------------------------- dbpedia reserach ------------------------------------

# replace blank spaces with backlash
corr_entity_list = []
for entity in entity_list:
    corr_ent = entity.replace(" ", "_")
    corr_entity_list.append(corr_ent)
#print(corr_entity_list)

# construct graph for each entity found in dbpedia
for corr_ent in corr_entity_list:
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")
    sparql.setQuery(
    """
     PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
     PREFIX dbo:<http://dbpedia.org/ontology/>

     CONSTRUCT {<http://dbpedia.org/resource/"""+"{}".format(corr_ent)+"""> ?p ?x . ?y ?q <http://dbpedia.org/resource/"""+"{}".format(corr_ent)+""">.
     <http://dbpedia.org/resource/"""+"{}".format(corr_ent)+"""> rdfs:label ?label ;
                                                                 rdfs:comment ?comment .
     }
     WHERE {
     {<http://dbpedia.org/resource/"""+"{}".format(corr_ent)+"""> ?p ?x}
     UNION
     {?y ?q <http://dbpedia.org/resource/"""+"{}".format(corr_ent)+""">
     FILTER (?p != "<http://www.w3.org/2000/01/rdf-schema#label>")
     FILTER (?p != "<http://www.w3.org/2000/01/rdf-schema#comment>")
     }

     <http://dbpedia.org/resource/"""+"{}".format(corr_ent)+"""> rdfs:label ?label ;
                                                                 rdfs:comment ?comment .
     FILTER (lang(?label) = "it") .
     FILTER (lang(?comment) = "it") .
     }

    """)

    sparql.setReturnFormat(TURTLE)
    results = sparql.query().convert()
    g = Graph()
    g.parse(data=results, format="turtle")
    generated_bk = g.serialize(format='turtle')

    file = open("C:/Users/us/Desktop/DHDK/a.a.2019-2020/Tesi/extraction/spacy/KG background knowledge/graph_bk.ttl","ab")
    file.write(generated_bk)
    file.close()
