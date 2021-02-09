# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 14:38:11 2020 

@author: e.peruch
"""
import spacy 
import itertools 

########basic processing on text#######
def doc_nlp(param):
    """This function reads a text file 
    with the nlp library spaCy for Italian language"""
    nlp = spacy.load('it_core_news_sm')
    with open(param["input_text"], "r", encoding="utf-8") as f:
        text = f.read()
    doc = nlp(text)
    return doc 

def ents_nlp(dspacy):
    ents_list = []
    for e in dspacy.ents:
        ents_list.append(e)
    return ents_list

def read_txt(dspacy): 
    """This function iterates over the sentences 
    of doc and collects them in a list"""
    list_sent = []
    for sent in dspacy.sents:
        list_sent.append(sent) 
    return list_sent

def split_dict(x, chunks):   
    """This function splits a dictionary
    into equal parts"""   
    i = itertools.cycle(range(chunks))       
    split = [dict() for _ in range(chunks)]
    for k, v in x.items():
        split[next(i)][str(k)] = (v)
    return split 