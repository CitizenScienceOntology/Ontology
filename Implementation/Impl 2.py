from rdflib.graph import Graph, URIRef
import matplotlib.pyplot as plt
import gzip
from rdflib import Graph
import random
from gastrodon import LocalEndpoint,one,QName
import pandas as pd
import numpy as np
np.random.seed(5)
from nltk.corpus import wordnet
g = Graph()


g.parse("Ont.owl", format="ttl")

#print(len(g))

m = open("Paul.txt", "w")

pd.DataFrame()
#for a, b, c, in g:
 #   m.write(a)

e=LocalEndpoint(g)

qres = e.select(
    """
    SELECT  ?s
       WHERE {
          ?s ?p ?o .
       }""")
#print(qres)
df = pd.DataFrame(qres)
random.randrange(20)
#b = random.sample((list(df.iloc[:],20)))
c = df.iloc[:19,-1]
#a = df.iloc[np.random.choice((df.iloc[:],21)),-1]
fit = open("WordMeaning.txt","r+")
#for i in fit:
   # print(i)
#print(fit)
pit = "xylem","xerophyte","concept","whorl","weed","vessel","vein","coniferous forest"

def WordsMeanng (c):
        for a in c:
            i=str(a)
             #  i= g.strip()[:-1]
            t = str(str(i)+"."+"n"+"."+"01")
            print(wordnet.synset(t).definition())
WordsMeanng(pit)
#df.to_csv('example.csv')
  #  str(a)
   # k = set(a)
   # W = random.sample(k,20)
   # print(W)

'''import pprint
for stmt in g:
    pprint.pprint(stmt)
'''
