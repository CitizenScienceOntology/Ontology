import rdflib
from rdflib.graph import Graph, URIRef
import matplotlib.pyplot as plt
import gzip
NewText = open("M.txt", "w")
from gastrodon import LocalEndpoint,one,QName

#g = rdflib.ConjunctiveGraph()
g = Graph()

g.parse("C:/publish/RDF/Birds.ttl",format="ttl")
len(g)

e=LocalEndpoint(g)


Q1=e.select("""

SELECT (Distinct ?o as ?Land_Information)
WHERE
{
?s ?p "San Francisco" .
?s <http://www.semanticweb.org/yawfrimpong/ontologies/untitled-ontology-13#FoundOn> ?o .
}
""")

Q1
print(Q1)
a =str(Q1)
NewText.write(a)
