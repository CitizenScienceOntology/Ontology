import rdflib
import ontospy
from owlready import *

a = ontospy.Ontospy("http://xmlns.com/foaf/0.1/")
g = rdflib.Graph()
result = g.parse("http://xmlns.com/foaf/0.1/")
print(a.classes)

for subj, pred, obj in g:
   if (subj, pred, obj) not in g:
       raise Exception("It better be!")
s = g.serialize(format='n3')

for subj in g:
     print(subj)
