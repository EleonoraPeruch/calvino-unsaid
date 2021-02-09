
from rdflib import URIRef, Literal, Graph
from .prefixes import NIF, XSD, ITSRDF, RDF
from .prefixes import NIFPrefixes

class NIFPhrase(object):
    """
    Represents an annotation in a document.
    """

    def __init__(self,
            context = None,
            annotator = None,
            mention = None,
            beginIndex = None,
            endIndex = None,
            score = None,
            taIdentRef = None,
            taClassRef = None,
            taMsClassRef = None,
            dependencyRelationType = None,
            dependency = None,
            uri = None,
            source = None):
        self.context = context
        self.annotator = annotator
        self.mention = mention
        self.beginIndex = beginIndex
        self.endIndex = endIndex
        self.score = score
        self.taIdentRef = taIdentRef
        self.taClassRef = taClassRef
        self.taMsClassRef = taMsClassRef
        self.dependencyRelationType = dependencyRelationType
        self.dependency = dependency
        self.original_uri = uri
        self.source = source

    @property
    def uri(self):
        return URIRef(self.original_uri or self.generated_uri)

    @property
    def generated_uri(self):
        return self.context.split('#')[0] + '#offset_' + str(self.beginIndex) + '_' + str(self.endIndex-1)

    def triples(self):
        """
        Returns the representation of the phrase as RDF triples
        """
        yield (self.uri, RDF.type, NIF.OffsetBasedString)
        yield (self.uri, RDF.type, NIF.Phrase)
        yield (self.uri, NIF.anchorOf, Literal(self.mention, datatype=XSD.string))
        yield (self.uri, NIF.beginIndex, Literal(self.beginIndex, datatype=XSD.nonNegativeInteger))
        yield (self.uri, NIF.endIndex, Literal(self.endIndex-1, datatype=XSD.nonNegativeInteger))

        if self.annotator is not None:
            yield (self.uri, ITSRDF.taAnnotatorsRef, URIRef(self.annotator))
        if self.score is not None:
            yield (self.uri, ITSRDF.taConfidence, Literal(str(float(self.score)), datatype=XSD.double, normalize=False))
        if self.taIdentRef is not None:
            yield (self.uri, ITSRDF.taIdentRef, URIRef(self.taIdentRef))
        if self.taMsClassRef is not None:
            yield (self.uri, NIF.taMsClassRef, URIRef(self.taMsClassRef))
        for currentClassRef in self.taClassRef or []:
            yield (self.uri, ITSRDF.taClassRef, URIRef(currentClassRef))
        if self.context is not None:
            yield (self.uri, NIF.referenceContext, URIRef(self.context))
        if self.taMsClassRef is not None:
            yield (self.uri, NIF.taMsClassRef, URIRef(self.taMsClassRef))
        if self.dependencyRelationType is not None:
            yield (self.uri, NIF.dependencyRelationType, Literal(self.dependencyRelationType, datatype=XSD.string))

        #if self.dependency is not None:
        #    yield (self.uri, NIF.dependency, Literal(self.dependency, datatype=XSD.string))

        if self.dependency is not None:
            yield (self.uri, NIF.dependency, URIRef(self.dependency))

        if self.source is not None:
            yield (self.uri, ITSRDF.taSource, Literal(self.source, datatype=XSD.string))

    @classmethod
    def load_from_graph(cls, graph, uri):
        """
        Given a RDF graph and a URI which represents a phrase in
        that graph, load the corresponding phrase.
        """
        phrase = cls()
        phrase.original_uri = uri
        for s,p,o in graph.triples((uri, None, None)):
            if p == NIF.anchorOf:
                phrase.mention = o.toPython()
            elif p == NIF.beginIndex:
                phrase.beginIndex = o.toPython()
            elif p == NIF.endIndex:
                phrase.endIndex = o.toPython()
            elif p == NIF.referenceContext:
                phrase.context = o.toPython()
            elif p == ITSRDF.taAnnotatorsRef:
                phrase.annotator = o.toPython()
            elif p == ITSRDF.taConfidence:
                phrase.score = o.toPython()
            elif p == ITSRDF.taIdentRef:
                phrase.taIdentRef = o.toPython()
            elif p == NIF.taMsClassRef:
                phrase.taMsClassRef = o.toPython()
            elif p == NIF.dependencyRelationType:
                phrase.dependencyRelationType = o.toPython()
            elif p == NIF.dependency:
                phrase.dependency = o.toPython()
            elif p == ITSRDF.taClassRef:
                if phrase.taClassRef is None:
                    phrase.taClassRef = []
                phrase.taClassRef.append(o.toPython())
            elif p == ITSRDF.taSource:
                phrase.source = o.toPython()
        return phrase

    @property
    def turtle(self):
        graph = Graph()
        for triple in self.triples():
            graph.add(triple)

        graph.namespace_manager = NIFPrefixes().manager
        return graph.serialize(format='turtle')

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        if (self.mention is not None
            and self.beginIndex is not None
            and self.endIndex is not None):
            mention = self.mention
            if len(mention) > 50:
                mention = mention[:50]+'...'
            return '<NIFPhrase {}-{}: {}>'.format(self.beginIndex, self.endIndex, repr(mention))
        else:
            return '<NIFPhrase (undefined)>'

    def _tuple(self):
        return (self.context,
        self.annotator,
        self.mention,
        self.beginIndex,
        self.endIndex,
        self.score,
        self.taIdentRef,
        set(self.taClassRef) if self.taClassRef else set(),
        self.taMsClassRef,
        self.dependencyRelationType,
        self.dependency,
        self.uri,
        self.source)

    def __eq__(self, other):
        return self._tuple() == other._tuple()

    def __hash__(self):
        return hash(self.uri)
