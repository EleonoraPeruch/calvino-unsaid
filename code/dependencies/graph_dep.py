# -*- coding: utf-8 -*-
import spacy
from spacy.symbols import nsubj, csubj, punct, mark, amod, cc, VERB, PRON
import it_core_news_sm

from rdflib import Graph, URIRef, BNode, Literal, Namespace

import sys
from dependencies_updated import up_dep

n = Namespace("http://uno.org/")

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


#print(g_up.serialize(format="turtle").decode("utf-8"))
generated_up = g_up.serialize(format="turtle").decode("utf-8")
file = open("C:/Users/us/Desktop/DHDK/a.a.2019-2020/Tesi/extraction/spacy/KG_dependencies/dependencies.ttl","w")
file.write(generated_up)
file.close()
