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


Q1=e.select("""

SELECT ?o (COUNT(?o) as ?oCount)
WHERE
{
  ?s <http://www.semanticweb.org/yawfrimpong/ontologies/untitled-ontology-13#FoundIn> ?o .
}
GROUP BY ?p
'ORDER BY DESC(?oCount)'
Limit 1
    """)

Q1
print(Q1)


