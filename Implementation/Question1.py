import rdflib
from rdflib.graph import Graph, URIRef
import matplotlib.pyplot as plt
import gzip

NewText = open("M.txt", "w")

from gastrodon import LocalEndpoint,one,QName

#g = rdflib.ConjunctiveGraph()
g = Graph()

g.parse("C:/publish/RDF/WSP1WS8.ttl",format="ttl")
len(g)

e=LocalEndpoint(g)

properties1=e.select("""

SELECT ?o
 {
      ?s '<http://www.semanticweb.org/yawfrimpong/ontologies/untitled-ontology-13#FoundIn>' ?o .
   } 
    """)

properties1

print(properties1)


#print(g.serialize(destination='D:/git/silk/data/staat.rdf',format="application/rdf+xml"))
'''
query = g.query(
    """CONSTRUCT {?s ?p ?o }
    WHERE {
      ?s ?p ?o .
      FILTER(STRSTARTS(STR(?p),"http://www.opengis.net/ont/geosparql#asWKT"))
   } """)
print(type(query))'''
#print(query.serialize(destination='D:/git/silk/data/staatWKT.ttl',format="ttl"))







