import rdflib
from rdflib.graph import Graph, URIRef
import matplotlib.pyplot as plt
import gzip
import numpy as np
import pandas as pd
from gastrodon import LocalEndpoint,one,QName

#g = rdflib.ConjunctiveGraph()
g = Graph()

g.parse("C:/publish/RDF/OWL.ttl",format="ttl")
len(g)

e=LocalEndpoint(g)
properties1=e.select("""

SELECT ?o ?o2
 {
        ?s <http://www.semanticweb.org/yawfrimpong/ontologies/\
        untitled-ontology-13#FeedOn> "GrassLand" . 
        ?s <http://www.semanticweb.org/yawfrimpong/ontologies/\
        untitled-ontology-13#HasLat> ?o . 
        ?s <http://www.semanticweb.org/yawfrimpong/ontologies/\
        untitled-ontology-13#FoundIn> "San Francisco" .
        ?s <http://www.semanticweb.org/yawfrimpong/ontologies/\
        untitled-ontology-13#HasName> "Owl" .
          }  """)
properties1
file = open("GrassLand.txt","w")
data = properties1.values
for row in data:
    file.write(str(row[0])+" "+str(row[1])+"\n")
file.close()
