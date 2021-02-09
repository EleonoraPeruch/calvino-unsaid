# -*- coding: utf-8 -*-
import spacy
from spacy_langdetect import LanguageDetector
import re
from spacy.symbols import nsubj, csubj, punct, mark, amod, cc, VERB, PRON
from spacy.pipeline import DependencyParser
from spacy.lang.it import Italian
import it_core_news_sm

nlp = spacy.load("it_core_news_sm")

lezione = "C:/Users/us/Desktop/DHDK/a.a.2019-2020/Tesi/extraction/spacy/KG_dependencies/la_leggerezza.txt"

with open(lezione, "r", encoding="utf-8") as f:
    text = f.read()
doc = nlp(text)

#for token in doc:
#    print( token.head.text, token.dep_, token.text, token.head.pos_, token._.language)
#            [child for child in token.children])

################################################################################
e_dep = {}
for token in doc:
    #start_idx =
    e_dep[str(token)] = {"token_head": token.head.text, "token_dep": token.dep_, "token_text": token.text, #"token_lang": token._.language,
    "token_children": [child.text for child in token.children], "token_start": token.idx, "token_end": (token.idx + len(token.text) - 1)} #, [child for child in token.children]
#print(e_dep)


#------------------INTERPRETATIVE----------------------#
verb_list = []
pron_list = []
for token in doc:
    if token.pos_ == "VERB" and ('Number=Plur|Person=2' in token.tag_ or 'Number=Plur|Person=1' in token.tag_ or 'Number=Sing|Person=2' in token.tag_  or 'Number=Sing|Person=1' in token.tag_):
        verb_list.append(token)
    elif token.pos_ == "PRON" and ('Number=Plur|Person=2' in token.tag_ or 'Number=Plur|Person=1' in token.tag_ or 'Number=Sing|Person=2' in token.tag_ or 'Number=Sing|Person=1' in token.tag_):
        pron_list.append(token)

list = []
p = re.findall(r"immagin\w+", doc.text)
for el in p:
    list.append(str(el))
#print(p)

keywords = ["luna", "volo", "salto", "secchio"]

verbs = []
prons = []
subj = ["io", "Io", "tu", "Tu", "noi", "Noi", "voi", "Voi"]
dep = {}
dep_verb = {}
dep_pron = {}
dep_rel = {}
dep_inter = {}
dep_adv = {}
dep_fin = {}
dep_comp = {}
dep_sem = {}


compl_v_sent = set()
compl_n_sent = set()

up_dep = {}
compl = {}

for sent in doc.sents:
    s = {}
    s["verb"] = {}
    s["pron"] = {}
    s["rel"] = {}
    s["inter"] = {}
    s["adv"] = {}
    s["fin"] = {}
    s["comp"] = {}
    s["sem"] = {}
    t = {}

################################# TEXTUAL CONNECTIVES ######################################
    # relative clauses
    for verb in sent:
            if verb.pos == VERB:
                head_start = verb.idx
                head_end = verb.idx + len(verb.text)
                for m in verb.children:
                    if m.dep == mark and str(m) == "che":
                        child_start = m.idx
                        child_end = m.idx + len(m.text)
                        s["rel"] = {"compl_v": {"head": verb.text, "dep": "mark", "child": "che",
                        "head_s": head_start, "head_e": head_end, "child_s": child_start, "child_e": child_end}}
                        dep_rel[sent] = s
                        up_dep.update(dep_rel)

                    elif m.dep == nsubj and str(m) == "che":
                        child_start = m.idx
                        child_end = m.idx + len(m.text)
                        s["rel"] = {"compl_n": {"head": verb.text, "dep": "nsubj", "child": "che",
                        "head_s": head_start, "head_e": head_end, "child_s": child_start, "child_e": child_end}}
                        dep_rel[sent] = s
                        up_dep.update(dep_rel)

    # interrogative clauses
    for int in sent:
        if int.dep_ in ("punct") and str(int) == "?":
            head_start = int.head.idx
            head_end = int.head.idx + len(int.head.text)
            child_start = int.idx
            child_end = int.idx + len(int.text)
            s["inter"] = {"head": int.head.text, "dep": int.dep_, "child": int.text,
            "head_s": head_start, "head_e": head_end, "child_s": child_start, "child_e": child_end}
            dep_inter[sent] = s
            up_dep.update(dep_inter)

    # adversative clauses
    for conj in sent:
        if conj.dep_ == cc and conj.text == "ma" or conj.text == "Ma":
            head_start = conj.head.idx
            head_end = conj.head.idx + len(conj.head.text)
            child_start = conj.idx
            child_end = conj.idx + len(conj.text)
            s["adv"] = {"head": conj.head.text, "dep": conj.dep_, "child": conj.text,
            "head_s": head_start, "head_e": head_end, "child_s": child_start, "child_e": child_end}
            dep_adv[sent] = s
            up_dep.update(dep_adv)

    # final clauses
    for word in sent:
        if word.text == "per" and word.dep == mark:
            head_start = word.head.idx
            head_end = word.head.idx + len(word.head.text)
            child_start = word.idx
            child_end = word.idx + len(word.text)
            s["fin"] = {"head": word.head.text, "dep": "mark", "child": word.text,
            "head_s": head_start, "head_e": head_end, "child_s": child_start, "child_e": child_end}
            dep_fin[sent] = s
            up_dep.update(dep_fin)

    # adverb of manner in similitudes
    for word in sent:
        if word.text == "come" and word.dep_ in ("case"):
            head_start = word.head.idx
            head_end = word.head.idx + len(word.head.text)
            child_start = word.idx
            child_end = word.idx + len(word.text)
            s["comp"] = {"head": word.head.text, "dep": "case", "child": word.text,
            "head_s": head_start, "head_e": head_end, "child_s": child_start, "child_e": child_end}
            dep_comp[sent] = s
            up_dep.update(dep_comp)

############################## MORPHOLOGICAL ELEMENTS ############################################
    # 1st and 2nd sing and plu verbs
    for verb in sent:
        if verb.pos == VERB and verb in verb_list:
            for poss_subj in verb.children:
                if poss_subj.dep == nsubj:
                    head_start = poss_subj.head.idx
                    head_end = (poss_subj.head.idx + len(poss_subj.head.text))
                    child_start = poss_subj.idx
                    child_end = (poss_subj.idx + len(poss_subj.text))
                    s["verb"] = {"head": poss_subj.head.text, "dep": poss_subj.dep_, "child": poss_subj.text,
                    "head_s": head_start, "head_e": head_end, "child_s": child_start, "child_e": child_end}
                    dep_verb[sent] = s
                    up_dep.update(dep_verb)


    # 1st and 2nd sing and plu pronouns
    for pron in sent:
        if pron in pron_list:
            if len(prons) == 0:
                n = len(dep)-1
            else:
                n = n+1
            prons.append(pron)
            head_start = pron.head.idx
            head_end = (pron.head.idx + len(pron.head.text))
            child_start = pron.idx
            child_end = (pron.idx + len(pron.text))
            s["pron"] = {"head": pron.head.text, "dep": pron.dep_, "child":pron.text,
            "head_s": head_start, "head_e": head_end, "child_s": child_start, "child_e": child_end}
            dep_pron[sent] = s
            up_dep.update(dep_pron)

######################################### LEXIS ##################################################
    # semantically relevant words
    #p = re.findall(r"immagin\w+", sent.text)
    #print(p)
    if len(p) != 0:
        for word in sent:
            for l in list:
                if word.text == str(l):

                    head_start = word.head.idx
                    head_end = (word.head.idx + len(word.head.text))
                    child_start = word.idx
                    child_end = (word.idx + len(word.text))

                    t[word.text] = {"head": word.head.text, "dep": word.dep_, "child": word.text,
                    "head_s": head_start, "head_e": head_end, "child_s": child_start, "child_e": child_end}
                    (s["sem"]).update(t)
                    dep_sem[sent] = s
                    up_dep.update(dep_sem)
            for el in keywords:
                if word.text == str(el):

                    head_start = word.head.idx
                    head_end = (word.head.idx + len(word.head.text))
                    child_start = word.idx
                    child_end = (word.idx + len(word.text))

                    t[word.text] = {"head": word.head.text, "dep": word.dep_, "child": word.text,
                    "head_s": head_start, "head_e": head_end, "child_s": child_start, "child_e": child_end}
                    (s["sem"]).update(t)
                    dep_sem[sent] = s
                    up_dep.update(dep_sem)

#print(dep_sem)
#print(up_dep)
#print(dep)