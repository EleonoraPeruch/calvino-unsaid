import spacy
import sys
sys.path.append('C:/Users/us/Documents/GitHub/pynif')
import pynif # original pynif package: https://pypi.org/project/pynif/

from pynif import NIFCollection, NIFPhrase, NIFContext

from pruning import entity_list
from dependencies_updated import up_dep

nlp = spacy.load("it_core_news_sm")
collection = NIFCollection(uri="https://github.com/EleonoraPeruch/calvino-unsaid/blob/master/texts")

my_context = "C:/Users/us/Desktop/DHDK/a.a.2019-2020/Tesi/extraction/spacy/la_leggerezza.txt"
with open(my_context, "r", encoding="utf8") as f:
    text = f.read()
doc = nlp(text)

context = collection.add_context(
   uri="https://github.com/EleonoraPeruch/calvino-unsaid/blob/master/texts/la_leggerezza.txt",
   mention=doc.text)

################################# NAMED ENTITIES ################################################
for token in doc:
    # named entities from spacy + named entities from tagme
    for key in entity_list:
        if key == token.text:
            id = key.replace(" ", "_")
            begin = token.idx
            end = token.idx + len(token.text)

            context.add_phrase(
                beginIndex=begin,
                endIndex=end,
                annotator='https://github.com/EleonoraPeruch',
                taIdentRef=''"http://dbpedia.org/resource/"+"{}".format(id)+''
            )

            for k, v in up_dep.items(): # ITERATE OVER "CHILD" IN EVERY DICT --> CHILD == KEY
                for ke, va in v.items():
                    if (ke == "verb" or ke == "pron" or ke == "inter" or ke == "adv" or
                    ke == "fin" or ke == "comp") and len(va) != 0 and va["child"] == key:
                        deptype = va["dep"] # indica la dipendenza che ha l'entity (CHILD) rispetto al sua token head (HEAD).
                        context.add_phrase(
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
                                context.add_phrase(
                                    beginIndex=begin,
                                    endIndex=end,
                                    dependencyRelationType=deptype, # type of dependency of the key wrt its token head.
                                    annotator='https://github.com/EleonoraPeruch'
                                    )

            for k, v in up_dep.items(): # ITERATE OVER "CHILD" IN EVERY DICT --> CHILD == KEY
                for ke, va in v.items():
                    if (ke == "verb" or ke == "pron" or ke == "inter" or ke == "adv" or
                    ke == "fin" or ke == "comp") and len(va) != 0 and va["head"] == key:
                        s = va["child_s"]
                        f = va["child_e"]
                        context.add_phrase(
                            beginIndex=begin,
                            endIndex=end,
                            dependency=''"https://github.com/EleonoraPeruch/calvino-unsaid/blob/master/texts/la_leggerezza.txt#offset"+"_"+"{}".format(s)+"_"+"{}".format(f)+'',
                            # children are the immediate syntactic dependents of the token (anchorOf). Key = governor
                            annotator='https://github.com/EleonoraPeruch'
                            )


                    elif ke == "rel" or ke == "sem":
                        for kee, vaa in va.items():
                            if vaa["head"] == key:
                                s = va["child_s"]
                                f = va["child_e"]
                                context.add_phrase(
                                    beginIndex=begin,
                                    endIndex=end,
                                    dependency=''"https://github.com/EleonoraPeruch/calvino-unsaid/blob/master/texts/la_leggerezza.txt#offset"+"_"+"{}".format(s)+"_"+"{}".format(f)+'',
                                    # children are the immediate syntactic dependents of the token (anchorOf). Key = governor
                                    annotator='https://github.com/EleonoraPeruch'
                                    )


###################################### DEPENDENCIES ###################################
for key, value in up_dep.items(): # ITERATE OVER "CHILD" IN EVERY DICT --> CHILD == KEY
    for k, v in value.items():
        if (k == "verb" or k == "pron" or k == "inter" or k == "adv" or
        k == "fin" or k == "comp") and len(v) != 0:
            begin = v["child_s"]
            end = v["child_e"]
            deptype = v["dep"]
            c = v["child"]

            for k, v in value.items():
                if len(v) > 1 and v["head"] == c:
                    s = v["child_s"]
                    f = v["child_e"]-1
                    context.add_phrase(
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
                            fi = va["child_e"]-1
                            context.add_phrase(
                                beginIndex=begin,
                                endIndex=end,
                                dependencyRelationType=deptype, # type of dependency of the key wrt its token head.
                                dependency=''"https://github.com/EleonoraPeruch/calvino-unsaid/blob/master/texts/la_leggerezza.txt#offset"+"_"+"{}".format(st)+"_"+"{}".format(fi)+'',
                                # children are the immediate syntactic dependents of the token (anchorOf). Key = governor
                                # --> if CHILD is HEAD in another triple, put here its CHILD in that triple
                                annotator='https://github.com/EleonoraPeruch'
                                )

        context.add_phrase(
            beginIndex=begin,
            endIndex=end,
            dependencyRelationType=deptype, # type of dependency of the key wrt its token head.
            annotator='https://github.com/EleonoraPeruch'
            )

for key, value in up_dep.items(): # ITERATE OVER "CHILD" IN EVERY DICT --> CHILD == KEY
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
                        fi = va["child_e"]-1
                        context.add_phrase(
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
                                f = v["child_e"]-1
                                context.add_phrase(
                                    beginIndex=begin,
                                    endIndex=end,
                                    dependencyRelationType=deptype, # type of dependency of the key wrt its token head.
                                    dependency=''"https://github.com/EleonoraPeruch/calvino-unsaid/blob/master/texts/la_leggerezza.txt#offset"+"_"+"{}".format(s)+"_"+"{}".format(f)+'',
                                    # children are the immediate syntactic dependents of the token (anchorOf). Key = governor
                                    annotator='https://github.com/EleonoraPeruch'
                                    )

            context.add_phrase(
                beginIndex=begin,
                endIndex=end,
                dependencyRelationType=deptype, # type of dependency of the key wrt its token head.
                annotator='https://github.com/EleonoraPeruch'
                )

###############################################################################

generated_nif = collection.dumps(format='turtle')
#print(generated_nif)

file = open("C:/Users/us/Desktop/DHDK/a.a.2019-2020/Tesi/extraction/spacy/KG_annotation/graph_ann_final.ttl","w")
file.write(generated_nif)
file.close()

########################TO PARSE IT BACK###############################
#parsed_collection = NIFCollection.loads(generated_nif, format='turtle')
#for context in parsed_collection.contexts:
#   for phrase in context.phrases:
#       print(phrase)
