import rdflib
from rdflib.graph import Graph, URIRef
import matplotlib.pyplot as plt
import gzip
from gastrodon import LocalEndpoint,one,QName

#g = rdflib.ConjunctiveGraph()
g = Graph()

g.parse("WSP1WS718295.ttl",format="n3")
len(g)
print(len(g))

e=LocalEndpoint(g)

properties1=e.select("""
   SELECT *
      
""")
properties1
print(properties1)

print(e.namespaces())

