# -*- coding: utf-8 -*-

from inout import doc_nlp, ents_nlp, read_txt, split_dict
from analyzer import verbs, prons, lexis, dep_parsing, spacy_ne, tagme_ne, pruning
from triplifier import ne_to_rdf, dep_to_rdf, nif_init, ne_to_nif, dep_to_nif, nif_to_rdf
from visualizer import text_to_xml, xml_to_html
from mpi4py import MPI
import numpy as np

import yaml
my_yaml_file = open("config.yaml")
param = yaml.load(my_yaml_file, Loader=yaml.FullLoader)

import sys
sys.path.append(param["pynif_python_path"])
import pynif
from pynif import NIFCollection, NIFPhrase, NIFContext
collection = NIFCollection(uri="https://github.com/EleonoraPeruch/calvino-unsaid/blob/master/texts")

comm = MPI.COMM_WORLD
rank = comm.Get_rank() 
size = comm.Get_size()

if rank == 0:
    dspacy = doc_nlp(param)
    text_ents = ents_nlp(dspacy)
    text_seg = read_txt(dspacy)
    sne = spacy_ne(text_ents)
    tne = tagme_ne(text_seg, param) 
    all_ne = pruning(sne, tne)
    relevant_lex = lexis(dspacy, param)
    relevant_verb = verbs(dspacy)
    relevant_pron = prons(dspacy)
    all_dep = dep_parsing(text_seg, relevant_lex, relevant_verb, relevant_pron)

    data_e = []
    send_count = len(all_ne) // size
    rest = len(all_ne) % size
    for s in range(size):
        start = s * send_count
        end = start + send_count 
        if rank == size - 1:
            data_e.append(all_ne[start:end+rest])
        else: 
            data_e.append(all_ne[start:end])
    
    data_d = split_dict(all_dep, chunks=size)

else:
    data_e = None
    data_d = None
    dspacy = None

dspacy = comm.bcast(dspacy, root=0)

data_e = comm.scatter(data_e, root=0)
named_entities_rdf = ne_to_rdf(data_e, param) 
data_e = comm.gather(data_e, root=0)

if rank == 0:
    dependencies_rdf = dep_to_rdf(all_dep, param) 
    ctx = nif_init(dspacy, collection)
else:
    ctx = None

ctx = comm.bcast(ctx, root=0)
#scatter delle due liste --> array divisa in sotto array dati i processori
#gather --> dati tanti array sui processori lo riporta al processore 0
data_e = comm.scatter(data_e, root=0)
data_d = comm.scatter(data_d, root=0)

ne_nif = ne_to_nif(dspacy, data_e, data_d, ctx)
dep_nif = dep_to_nif(data_d, ctx)

data_e = comm.gather(data_e, root=0)
data_d = comm.gather(data_d, root=0)

if rank == 0: 
    nif_encoding_rdf = nif_to_rdf(param, collection)
    xml_encoding = text_to_xml(param)
    html_encoding = xml_to_html(xml_encoding, param)





#no parallelisation

"""
dspacy = doc_nlp(param)
text_ents = ents_nlp(dspacy)
text_seg = read_txt(dspacy)

sne = spacy_ne(text_ents)
tne = tagme_ne(text_seg, param) 
all_ne = pruning(sne, tne)
relevant_lex = lexis(dspacy, param)
relevant_verb = verbs(dspacy)
relevant_pron = prons(dspacy)
all_dep = dep_parsing(text_seg, relevant_lex, relevant_verb, relevant_pron)

named_entities_rdf = ne_to_rdf(all_ne, param) 
dependencies_rdf = dep_to_rdf(all_dep, param) 
ctx = nif_init(dspacy, collection)
ne_nif = ne_to_nif(dspacy, all_ne, all_dep, ctx)
dep_nif = dep_to_nif(all_dep, ctx)
nif_encoding_rdf = nif_to_rdf(param, collection)

xml_encoding = text_to_xml(param)
html_encoding = xml_to_html(xml_encoding, param)
"""
