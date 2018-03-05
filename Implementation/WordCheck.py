import numpy as np
np.random.seed(5)
from nltk.corpus import wordnet
import rdflib
from rdflib.graph import *
from gastrodon import LocalEndpoint,one,QName

Ont = Graph()
Ont.parse("C:/publish/RDF/OWL.ttl",format="ttl")
OpenOnto = open("OntClasses.txt","w")
len(Ont)
e=LocalEndpoint(Ont)

Classes=e.select("""
SELECT  ?s
WHERE
{
?s ?p ?o .
}
""")

print(Classes)

pit = "Desert"
p= "Mangrove","adaptation","Biome","Desert","Community","Conservation","habitat","Species","City","Population","Taxon","Nomenclature","Landscape","Extinction","Diversity","Ecology","Environment","Watershed","Seagrass","Assemblage"
def WordsMeanng (c):
        for a in c:
            i=str(a)
             #  i= g.strip()[:-1]
            t = str(str(i)+"."+"n"+"."+"01")
            print(wordnet.synset(t).definition())
            print("*****************************************************")
#WordsMeanng(pit)

def WM (c):
    a= str(c)
    t = str(str(a)+"."+"n"+"."+"01")
    print(wordnet.synset(t).definition())
    print("*****************************************************")
#WM(pit)

