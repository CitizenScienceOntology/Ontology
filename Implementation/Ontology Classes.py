import rdflib
from rdflib.graph import Graph, URIRef
import matplotlib.pyplot as plt
import gzip
NewText = open("M.txt", "w")
from gastrodon import LocalEndpoint,one,QName

#g = rdflib.ConjunctiveGraph()
g = Graph()

g.parse("C:/publish/Ontology.ttl",format="ttl")
len(g)

e=LocalEndpoint(g)


Q1=e.select("""

SELECT ?p
WHERE
{
?s ?p ?o .
}
""")

Q1
print(Q1)
a =str(Q1)
NewText.write(a)
