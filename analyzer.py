# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 14:38:26 2020

@author: e.peruch 
""" 
 
import json
import requests 
import re
import spacy
import it_core_news_sm
from spacy.symbols import nsubj, csubj, punct, mark, amod, cc, VERB, PRON
import time


def spacy_ne(text_ents):
    """This function collects the doc named entities
    and their corresponding starting and ending
    character in a dictionary"""
    named_entity_dict = {}
    for e in text_ents:
        named_entity_dict[str(e)] = (e.start_char, e.end_char)
    return named_entity_dict


def tagme_ne(text_seg, param): 
    """This function analyses the input with tagme
    and collects the request output in a dictionary
    that is used to create a json file"""
    data_tag = []
    for sent in text_seg:
        r = requests.get("https://tagme.d4science.org/tagme/tag?lang=it&include_abstract=false&include_categories=true&gcube-token="+param["tagme_token"]+"&text="+sent.text)
        data_tag.append(json.loads(r.text))

    dict_tagme = {param["lecture"]: data_tag}
    with open("tagme_data.json", "w", encoding="utf8") as output:
        json.dump(dict_tagme, output, indent=4, ensure_ascii=False)
    return dict_tagme


def pruning(sne, tne):
    """This function performs the pruning over
    the named entities identified through spaCy
    and Tagme"""
    entity_list = []
    for k, v in tne.items():
        for dtag in tne[k]:
            for dict_min in dtag["annotations"]:
                for key, value in sne.items():
                    if key in dict_min["title"]:
                        if int(dict_min["end"] - dict_min["start"]) == int(sne[key][1] - sne[key][0]) and dict_min["title"] not in entity_list:
                            entity_list.append(dict_min["title"])
    return entity_list

def verbs(dspacy):
    """This function identifies the relevant verbs
    in doc and collects them in a list"""
    verb_list = []
    for token in dspacy:
        if token.pos_ == "VERB" and ('Number=Plur|Person=2' in token.tag_ or 'Number=Plur|Person=1' in token.tag_ or 'Number=Sing|Person=2' in token.tag_  or 'Number=Sing|Person=1' in token.tag_):
            verb_list.append(token)
    return verb_list

def prons(dspacy):
    """This identifies the relevant pronouns
    in doc and collects them in a list"""
    pron_list = []
    for token in dspacy:
        if token.pos_ == "PRON" and ('Number=Plur|Person=2' in token.tag_ or 'Number=Plur|Person=1' in token.tag_ or 'Number=Sing|Person=2' in token.tag_ or 'Number=Sing|Person=1' in token.tag_):
            pron_list.append(token)
    return pron_list


def lexis(dspacy, param):
    """This function identifies some relevant 
    lexis in doc and collects it in a list"""
    p = re.findall(param["keywords_regex"], dspacy.text)
    for el in p:
        param["keywords"].append(str(el))
    return param["keywords"]



def dep_parsing(text_seg, relevant_lex, relevant_verb, relevant_pron):
    """This function collects the relevant
    morpho-syntactic and semantic elements in a 
    dictionary"""
    
    prons = []
    dep = {}
    dep_verb = {}
    dep_pron = {}
    dep_rel = {}
    dep_inter = {}
    dep_adv = {}
    dep_fin = {}
    dep_comp = {}
    dep_sem = {}
    
    up_dep = {}
    
    for sent in text_seg:
 
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
        for int_c in sent:
            if int_c.dep_ in ("punct") and str(int_c) == "?":
                head_start = int_c.head.idx
                head_end = int_c.head.idx + len(int_c.head.text) 
                child_start = int_c.idx
                child_end = int_c.idx + len(int_c.text)
                s["inter"] = {"head": int_c.head.text, "dep": int_c.dep_, "child": int_c.text,
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
            if verb.pos == VERB and verb in relevant_verb:
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
            if pron in relevant_pron:
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
        if len(relevant_lex) != 0:
            for word in sent:
                for l in relevant_lex:
                    if word.text == str(l):
    
                        head_start = word.head.idx
                        head_end = (word.head.idx + len(word.head.text))
                        child_start = word.idx
                        child_end = (word.idx + len(word.text))
    
                        t[word.text] = {"head": word.head.text, "dep": word.dep_, "child": word.text,
                        "head_s": head_start, "head_e": head_end, "child_s": child_start, "child_e": child_end}
                        (s["sem"]).update(t)
                        dep_sem[sent] = s
    return up_dep
