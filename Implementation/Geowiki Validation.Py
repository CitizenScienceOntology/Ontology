	
	#Importing Modules
	import rdflib
	from rdflib.graph import Graph, URIRef
	import matplotlib.pyplot as plt
	import gzip
	#Loading the Combined Dataset
	from gastrodon import LocalEndpoint,one,QName
	#g = rdflib.ConjunctiveGraph()
	g = Graph()
	#g.parse("C:/publish/RDF/OWL.ttl",format="ttl")
	g.parse("C:/publish/RDF/WSP1WS8.ttl",format="ttl")
	len(g)
	e=LocalEndpoint(g)
	#Query formulation
	properties1=e.select("""
	SELECT ?o ?o1 ?o2
	WHERE { 
	?s <http://www.semanticweb.org/
	\yawfrimpong/ontologies/untitled-ontology-13#FoundOn>  ?o .
	?s <http://www.semanticweb.org/yawfrimpong/ontologies\
	/untitled-ontology-13#HasLat> ?o1 .
	?s <http://www.semanticweb.org/yawfrimpong/ontologies\
	/untitled-ontology-13#HasLong> ?o2 . 
	?s <http://www.semanticweb.org/yawfrimpong/ontologies\
	/untitled-ontology-13#HasLong> "San Francisco" . 
	?s <http://www.semanticweb.org/yawfrimpong/ontologies\
	/untitled-ontology-13FeedOn#> "Forest" . 
	 }
		""")
	properties1
	#Saving and Printing Result
	print(properties1)








