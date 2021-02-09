pynif
=====

The `NLP Interchange Format
(NIF) <http://persistence.uni-leipzig.org/nlp2rdf/>`__ is an
RDF/OWL-based format that aims to achieve interoperability between
Natural Language Processing (NLP) tools, language resources and
annotations. It offers a standard representation of annotated texts for
tasks such as `Named Entity
Recognition <https://en.wikipedia.org/wiki/Named-entity_recognition>`__
or `Entity Linking <https://en.wikipedia.org/wiki/Entity_linking>`__. It
is used by `GERBIL <https://github.com/dice-group/gerbil>`__ to run
reproducible evaluations of annotators.

This Python library can be used to serialize and deserialized annotated
corpora in NIF.

Documentation
-------------

`NIF Documentation <http://persistence.uni-leipzig.org/nlp2rdf/>`__

Supported NIF versions
----------------------

NIF 2.1, serialized in `any of the formats supported by
rdflib <https://rdflib.readthedocs.io/en/stable/plugin_parsers.html>`__

Overview
--------

This library is revolves around three core classes: \* a ``NIFContext``
is a document (a string); \* a ``NIFPhrase`` is the annotation of a
snippet of text (usually a phrase) in a document; \* a ``NIFCollection``
is a set of documents, which constitutes a collection. In NIF, each of
these objects is identified by a URI, and their attributes and relations
are encoded by RDF triples between these URIs. This library abstracts
away the encoding by letting you manipulate collections, contexts and
phrases as plain Python objects.

Quickstart
-----------

0) Import and create a collection

.. code:: python

   from pynif import NIFCollection

   collection = NIFCollection(uri="http://freme-project.eu")
           

1) Create a context

.. code:: python

   context = collection.add_context(
       uri="http://freme-project.eu/doc32",
       mention="Diego Maradona is from Argentina.")

2) Create entries for the entities

.. code:: python

   context.add_phrase(
       beginIndex=0,
       endIndex=14,
       taClassRef=['http://dbpedia.org/ontology/SportsManager', 'http://dbpedia.org/ontology/Person', 'http://nerd.eurecom.fr/ontology#Person'],
       score=0.9869992701528016,
       annotator='http://freme-project.eu/tools/freme-ner',
       taIdentRef='http://dbpedia.org/resource/Diego_Maradona',
       taMsClassRef='http://dbpedia.org/ontology/SoccerManager')

   context.add_phrase(
       beginIndex=23,
       endIndex=32,
       taClassRef=['http://dbpedia.org/ontology/PopulatedPlace', 'http://nerd.eurecom.fr/ontology#Location',
       'http://dbpedia.org/ontology/Place'],
       score=0.9804963628413852,
       annotator='http://freme-project.eu/tools/freme-ner',
       taMsClassRef='http://dbpedia.org/resource/Argentina')

3) Finally, get the output with the format that you need

.. code:: python

   generated_nif = collection.dumps(format='turtle')
   print(generated_nif)

You will obtain the NIF representation as a string:

.. code:: turtle

   <http://freme-project.eu> a nif:ContextCollection ;
       nif:hasContext <http://freme-project.eu/doc32> ;
       ns1:conformsTo <http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core/2.1> .

   <http://freme-project.eu/doc32> a nif:Context,
           nif:OffsetBasedString ;
       nif:beginIndex "0"^^xsd:nonNegativeInteger ;
       nif:endIndex "33"^^xsd:nonNegativeInteger ;
       nif:isString "Diego Maradona is from Argentina." .

   <http://freme-project.eu/doc32#offset_0_14> a nif:OffsetBasedString,
           nif:Phrase ;
       nif:anchorOf "Diego Maradona" ;
       nif:beginIndex "0"^^xsd:nonNegativeInteger ;
       nif:endIndex "14"^^xsd:nonNegativeInteger ;
       nif:referenceContext <http://freme-project.eu/doc32> ;
       nif:taMsClassRef <http://dbpedia.org/ontology/SoccerManager> ;
       itsrdf:taAnnotatorsRef <http://freme-project.eu/tools/freme-ner> ;
       itsrdf:taClassRef <http://dbpedia.org/ontology/Person>,
           <http://dbpedia.org/ontology/SportsManager>,
           <http://nerd.eurecom.fr/ontology#Person> ;
       itsrdf:taConfidence 9.869993e-01 ;
       itsrdf:taIdentRef <http://dbpedia.org/resource/Diego_Maradona> .

   <http://freme-project.eu/doc32#offset_23_32> a nif:OffsetBasedString,
           nif:Phrase ;
       nif:anchorOf "Argentina" ;
       nif:beginIndex "23"^^xsd:nonNegativeInteger ;
       nif:endIndex "32"^^xsd:nonNegativeInteger ;
       nif:referenceContext <http://freme-project.eu/doc32> ;
       nif:taMsClassRef <http://dbpedia.org/resource/Argentina> ;
       itsrdf:taAnnotatorsRef <http://freme-project.eu/tools/freme-ner> ;
       itsrdf:taClassRef <http://dbpedia.org/ontology/Place>,
           <http://dbpedia.org/ontology/PopulatedPlace>,
           <http://nerd.eurecom.fr/ontology#Location> ;
       itsrdf:taConfidence 9.804964e-01 .

4) You can then parse it back:

.. code:: python

   parsed_collection = NIFCollection.loads(generated_nif, format='turtle')

   for context in parsed_collection.contexts:
      for phrase in context.phrases:
          print(phrase)

Issues
------

If you have any problems with or questions about this library, please
contact us through a `GitHub
issue <https://github.com/wetneb/pynif/issues>`__.
