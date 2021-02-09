# -*- coding: utf-8 -*-
""" 
Created on Tue Dec 29 14:43:38 2020

@author: e.peruch
"""

from SPARQLWrapper import SPARQLWrapper, TURTLE
import json
import spacy
import it_core_news_sm
import requests 
import rdflib
from rdflib import Graph, URIRef, BNode, Literal, Namespace
from rdflib.plugins import sparql
import os

def ne_to_rdf(all_ne, param):
    """This function performs sparql queries for all the
    named entities and collects results in a ttl graph"""
    #------------------ dbpedia research --------------------

    # replace blank spaces with backlash
    corr_entity_list = []
    for entity in all_ne:
        corr_ent = entity.replace(" ", "_")
        corr_entity_list.append(corr_ent)

    # construct graph for each entity found in dbpedia - online 
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
        generated_bk = g.serialize(format='turtle').decode("utf8")
       #os.makedirs(path, exist_ok=True)

        file_bk = open(param["bk_graph"],"w")
        file_bk.write(generated_bk)
        file_bk.close()
    return generated_bk
    

def dep_to_rdf(all_dep, param):
    """This function creates a ttl graph with 
    all the relevant dependencies"""
    g_up = Graph()
    for key, value in all_dep.items():
        for k, v in value.items():
            if k == "verb" and len(v) != 0:
                s = Literal(v["head"])
                p = URIRef("http://fginter.github.io/docs/u/dep/all.html#al-u-dep/"+"{}".format(v["dep"]))
                o = Literal(v["child"])
                g_up.add((s, p, o))
            if k == "pron" and len(v) != 0:
                s = Literal(v["head"])
                p = URIRef("http://fginter.github.io/docs/u/dep/all.html#al-u-dep/"+"{}".format(v["dep"]))
                o = Literal(v["child"])
                g_up.add((s, p, o))
            if k == "inter" and len(v) != 0:
                s = Literal(v["head"])
                p = URIRef("http://fginter.github.io/docs/u/dep/all.html#al-u-dep/"+"{}".format(v["dep"]))
                o = Literal(v["child"])
                g_up.add((s, p, o))
            if k == "adv" and len(v) != 0:
                s = Literal(v["head"])
                p = URIRef("http://fginter.github.io/docs/u/dep/all.html#al-u-dep/"+"{}".format(v["dep"]))
                o = Literal(v["child"])
                g_up.add((s, p, o))
            if k == "fin" and len(v) != 0:
                s = Literal(v["head"])
                p = URIRef("http://fginter.github.io/docs/u/dep/all.html#al-u-dep/"+"{}".format(v["dep"]))
                o = Literal(v["child"])
                g_up.add((s, p, o))
            if k == "comp" and len(v) != 0:
                s = Literal(v["head"])
                p = URIRef("http://fginter.github.io/docs/u/dep/all.html#al-u-dep/"+"{}".format(v["dep"]))
                o = Literal(v["child"])
                g_up.add((s, p, o))
            if k == "rel" and len(v) != 0:
                for ke, va in v.items():
                    s = Literal(va["head"])
                    p = URIRef("http://fginter.github.io/docs/u/dep/all.html#al-u-dep/"+"{}".format(va["dep"]))
                    o = Literal(va["child"])
                    g_up.add((s, p, o))
            if k == "sem" and len(v) != 0:
                for ke, va in v.items():
                    s = Literal(va["head"])
                    p = URIRef("http://fginter.github.io/docs/u/dep/all.html#al-u-dep/"+"{}".format(va["dep"]))
                    o = Literal(va["child"])
                    g_up.add((s, p, o))

    generated_up = g_up.serialize(format="turtle").decode("utf-8")
    file_dep = open(param["dep_graph"],"w")
    file_dep.write(generated_up)
    file_dep.close()
    return generated_up

#collection = NIFCollection(uri="https://github.com/EleonoraPeruch/calvino-unsaid/blob/master/texts")

def nif_init(dspacy, collection):
    """This function initializes the nif collection
    and adds a context"""
    context = collection.add_context(
    uri="https://github.com/EleonoraPeruch/calvino-unsaid/blob/master/texts/la_leggerezza.txt",
    mention=dspacy.text)
    return context

def ne_to_nif(dspacy, all_ne, all_dep, ctx):
    """This function adds the named entities 
    to the context in the collection"""
    for token in dspacy:
    # named entities from spacy + named entities from tagme
        for key in all_ne:
            if key == token.text:
                id = key.replace(" ", "_")
                begin = token.idx
                end = token.idx + len(token.text)

                ctx.add_phrase(
                    beginIndex=begin,
                    endIndex=end,
                    annotator='https://github.com/EleonoraPeruch',
                    taIdentRef=''"http://dbpedia.org/resource/"+"{}".format(id)+''
                )

                for k, v in all_dep.items(): # ITERATE OVER "CHILD" IN EVERY DICT --> CHILD == KEY
                    for ke, va in v.items():
                        if (ke == "verb" or ke == "pron" or ke == "inter" or ke == "adv" or
                        ke == "fin" or ke == "comp") and len(va) != 0 and va["child"] == key:
                            deptype = va["dep"] # indica la dipendenza che ha l'entity (CHILD) rispetto al sua token head (HEAD).
                            ctx.add_phrase(
                                beginIndex=begin,
                                endIndex=end,
                                dependencyRelationType=deptype, # type of dependency of the key wrt its token head.
                                annotator='https://github.com/EleonoraPeruch'
                                )

                        elif ke == "rel" or ke == "sem":
                            for kee, vaa in va.items():
                                if vaa["child"] == key:
                                    deptype = vaa["dep"]
                                    c = vaa["child"]
                                    ctx.add_phrase(
                                        beginIndex=begin,
                                        endIndex=end,
                                        dependencyRelationType=deptype, # type of dependency of the key wrt its token head.
                                        annotator='https://github.com/EleonoraPeruch'
                                        )

                for k, v in all_dep.items(): # ITERATE OVER "CHILD" IN EVERY DICT --> CHILD == KEY
                    for ke, va in v.items():
                        if (ke == "verb" or ke == "pron" or ke == "inter" or ke == "adv" or
                        ke == "fin" or ke == "comp") and len(va) != 0 and va["head"] == key:
                            s = va["child_s"]
                            f = va["child_e"]
                            ctx.add_phrase(
                                beginIndex=begin,
                                endIndex=end,
                                dependency=''"https://github.com/EleonoraPeruch/calvino-unsaid/blob/master/texts/la_leggerezza.txt#offset"+"_"+"{}".format(s)+"_"+"{}".format(f)+'',
                                # children are the immediate syntactic dependents of the token (anchorOf). Key = governor
                                annotator='https://github.com/EleonoraPeruch'
                                )


                        elif ke == "rel" or ke == "sem":
                            for kee, vaa in va.items():
                                if vaa["head"] == key:
                                    s = vaa["child_s"] ######
                                    f = vaa["child_e"] ######
                                    ctx.add_phrase(
                                        beginIndex=begin,
                                        endIndex=end,
                                        dependency=''"https://github.com/EleonoraPeruch/calvino-unsaid/blob/master/texts/la_leggerezza.txt#offset"+"_"+"{}".format(s)+"_"+"{}".format(f)+'',
                                        # children are the immediate syntactic dependents of the token (anchorOf). Key = governor
                                        annotator='https://github.com/EleonoraPeruch'
                                        )

    return ctx ####### context enhanced with phrases of ne ######################

def dep_to_nif(all_dep, ctx):
    """This function adds the dependencies
    to the context in the collection"""
    for key, value in all_dep.items(): # ITERATE OVER "CHILD" IN EVERY DICT --> CHILD == KEY
        for k, v in value.items():
            if (k == "verb" or k == "pron" or k == "inter" or k == "adv" or
            k == "fin" or k == "comp") and len(v) != 0:
                begin = v["child_s"]
                end = v["child_e"]
                deptype = v["dep"]
                c = v["child"]

                #for k, v in value.items():
                if len(v) > 1 and v["head"] == c:
                    s = v["child_s"]
                    f = v["child_e"]
                    ctx.add_phrase(
                        beginIndex=begin,
                        endIndex=end,
                        dependencyRelationType=deptype, # type of dependency of the key wrt its token head.
                        dependency=''"https://github.com/EleonoraPeruch/calvino-unsaid/blob/master/texts/la_leggerezza.txt#offset"+"_"+"{}".format(s)+"_"+"{}".format(f)+'',
                        # children are the immediate syntactic dependents of the token (anchorOf). Key = governor
                        # --> if CHILD is HEAD in another triple, put here its CHILD in that triple
                        annotator='https://github.com/EleonoraPeruch'
                        )

                elif k == "rel" or k == "sem":
                    for ke, va in v.items():
                        if len(va) != 0 and va["head"] == c:
                            st = va["child_s"]
                            fi = va["child_e"]
                            ctx.add_phrase(
                                beginIndex=begin,
                                endIndex=end,
                                dependencyRelationType=deptype, # type of dependency of the key wrt its token head.
                                dependency=''"https://github.com/EleonoraPeruch/calvino-unsaid/blob/master/texts/la_leggerezza.txt#offset"+"_"+"{}".format(st)+"_"+"{}".format(fi)+'',
                                # children are the immediate syntactic dependents of the token (anchorOf). Key = governor
                                # --> if CHILD is HEAD in another triple, put here its CHILD in that triple
                                annotator='https://github.com/EleonoraPeruch'
                                )

                ctx.add_phrase(
                    beginIndex=begin,
                    endIndex=end,
                    dependencyRelationType=deptype, # type of dependency of the key wrt its token head.
                    annotator='https://github.com/EleonoraPeruch'
                    )

    for key, value in all_dep.items(): # ITERATE OVER "CHILD" IN EVERY DICT --> CHILD == KEY
        for k, v in value.items():
            if (k == "rel" or k == "sem") and len(v) != 0:
                for ke, va in v.items():
                    begin = va["child_s"]
                    end = va["child_e"]
                    deptype = va["dep"]
                    c = va["child"]


                    for ke, va in v.items():
                        if len(va) > 1 and va["head"] == c:
                            st = va["child_s"]
                            fi = va["child_e"]
                            ctx.add_phrase(
                                beginIndex=begin,
                                endIndex=end,
                                dependencyRelationType=deptype, # type of dependency of the key wrt its token head.
                                dependency=''"https://github.com/EleonoraPeruch/calvino-unsaid/blob/master/texts/la_leggerezza.txt#offset"+"_"+"{}".format(st)+"_"+"{}".format(fi)+'',
                                # children are the immediate syntactic dependents of the token (anchorOf). Key = governor
                                annotator='https://github.com/EleonoraPeruch'
                                )

                        elif k == "verb" or k == "pron" or k == "inter" or k == "adv" or k == "fin" or k == "comp":
                            for k, v in value.items():
                                if len(v) != 0 and v["head"] == c:
                                    s = v["child_s"]
                                    f = v["child_e"]
                                    ctx.add_phrase(
                                        beginIndex=begin,
                                        endIndex=end,
                                        dependencyRelationType=deptype, # type of dependency of the key wrt its token head.
                                        dependency=''"https://github.com/EleonoraPeruch/calvino-unsaid/blob/master/texts/la_leggerezza.txt#offset"+"_"+"{}".format(s)+"_"+"{}".format(f)+'',
                                        # children are the immediate syntactic dependents of the token (anchorOf). Key = governor
                                        annotator='https://github.com/EleonoraPeruch'
                                        )

                    ctx.add_phrase(
                        beginIndex=begin,
                        endIndex=end,
                        dependencyRelationType=deptype, # type of dependency of the key wrt its token head.
                        annotator='https://github.com/EleonoraPeruch'
                        )
    return ctx ####### context enhanced with phrases of dep ################

def nif_to_rdf(param, collection):
    """This function collects all the data encoded 
    in nif in a ttl graph"""
    generated_nif = collection.dumps(format='turtle')
    file_nif = open(param["nif_graph"],"w")
    file_nif.write(generated_nif)
    file_nif.close()
    return generated_nif