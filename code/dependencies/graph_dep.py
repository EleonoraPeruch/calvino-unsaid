# -*- coding: utf-8 -*-
import spacy
from spacy.symbols import nsubj, csubj, punct, mark, amod, cc, VERB, PRON
import it_core_news_sm

from rdflib import Graph, URIRef, BNode, Literal, Namespace
#from rdflib.namespace import OWL, RDF

import sys
# insert at 1, 0 is the script path (or '' in REPL)
#from dependencies import dep, e_dep
from dependencies_updated import up_dep

n = Namespace("http://uno.org/")
#g = Graph()
#g.bind("uno", n)

########################### GRAPH WITH ALL DEPENDENCIES ###############################################
#g_e = Graph()
#g_e.bind("uno", n)

#for key, value in e_dep.items():
#    s = Literal(value["token_head"])
#    p = URIRef("http://fginter.github.io/docs/u/dep/all.html#al-u-dep/"+"{}".format(value["token_dep"]))
#    o = Literal(value["token_text"])
#    g_e.add((s, p, o))

#generated_e = g_e.serialize(format="turtle").decode("utf-8")
#file = open("C:/Users/us/Desktop/DHDK/a.a.2019-2020/Tesi/extraction/spacy/KG_dependencies/dependencies.ttl","w")
#file.write(generated_e)
#file.close()
########################################################################################################

############################# OLD GRAPH ################################################################
# passing values from the dependencies dict (dep_dict.txt)
#for key, value in dep.items():
#    s = Literal(key)  # passing a string
#    p = URIRef("http://fginter.github.io/docs/u/dep/all.html#al-u-dep/nsubj")
#    for k, v in value["verb-subj"].items():
#        if k in ("subj") and len(value["verb-subj"]["subj"]) != 0:
#            o = Literal(v)
#            g.add((s, p, o))

#    p = URIRef("http://fginter.github.io/docs/u/dep/all.html#al-u-dep/root")
#    for k, v in value["verb-subj"].items():
#        if k in ("verb") and len(value["verb-subj"]["verb"]) != 0:
#            o = Literal(v)
#            g.add((s, p, o))

#    p = URIRef("http://fginter.github.io/docs/u/pos/all.html#al-u-pos/pron")
#    o = Literal(value["pron"])
#    if len(value["pron"]) != 0:
#        g.add((s, p, o))

#    p = URIRef("http://fginter.github.io/docs/u/dep/all.html#al-u-dep/csubj")
#    for k, v in value["sub"].items():
#        if k in ("csubj") and len(value["sub"]["csubj"]) != 0:
#            o = Literal(v)
#            g.add((s, p, o))
#    p = URIRef("http://fginter.github.io/docs/u/dep/all.html#al-u-dep/xcomp")
#    for k, v in value["sub"].items():
#        if k in ("xcomp") and len(value["sub"]["xcomp"]) != 0:
#            o = Literal(v)
#            g.add((s, p, o))
#    p = URIRef("http://fginter.github.io/docs/u/dep/all.html#al-u-dep/ccomp")
#    for k, v in value["sub"].items():
#        if k in ("ccomp") and len(value["sub"]["ccomp"]) != 0:
#            o = Literal(v)
#            g.add((s, p, o))

#    p = URIRef("http://fginter.github.io/docs/u/dep/all.html#al-u-dep/conj")
#    for k, v in value["coord"].items():
#        if k in ("conj") and len(value["coord"]["conj"]) != 0:
#            o = Literal(v)
#            g.add((s, p, o))
#    p = URIRef("http://fginter.github.io/docs/u/dep/all.html#al-u-dep/cc")
#    for k, v in value["coord"].items():
#        if k in ("cc") and len(value["coord"]["cc"]) != 0:
#            o = Literal(v)
#            g.add((s, p, o))
#    p = URIRef("http://fginter.github.io/docs/u/dep/all.html#al-u-dep/punct")
#    for k, v in value["coord"].items():
#        if k in ("punct") and len(value["coord"]["punct"]) != 0:
#            o = Literal(v)
#            g.add((s, p, o))

#    s = Literal(value["cf"])
#    p = URIRef("http://fginter.github.io/docs/u/dep/all.html#al-u-dep/punct") # contains cross-reference
#    o = Literal("quotation marks")
#    if len(value["cf"]) != 0:
#        g.add((s, p, o))

#    s = Literal(value["ref"])
#    p = URIRef("http://fginter.github.io/docs/u/dep/all.html#al-u-dep/punct") # contains self_reflexive passage
#    o = Literal("?")
#    if len(value["ref"]) != 0:
#        g.add((s, p, o))

#    s = Literal(key)
#    p = URIRef("http://fginter.github.io/docs/u/dep/all.html#al-u-dep/nsubj") # contains repetition
#    o = Literal(value["rep"])
#    if len(value["rep"]) != 0:
#        g.add((s, p, o))

#for s, p, o in g.triples((s, p, o)):
#    if len(o) == 0 or o == []:
#        g.remove((s, p, o))

#print(g.serialize(format="turtle").decode("utf-8"))
########################################################################################################

################################# NEW GRAPH WITH SELECTED DEPENDENCIES #################################

g_up = Graph()
g_up.bind("uno", n)

for key, value in up_dep.items():
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


print(g_up.serialize(format="turtle").decode("utf-8"))
#generated_up = g_up.serialize(format="turtle").decode("utf-8")
#file = open("C:/Users/us/Desktop/DHDK/a.a.2019-2020/Tesi/extraction/spacy/KG_dependencies/dependencies.ttl","w")
#file.write(generated_up)
#file.close()
