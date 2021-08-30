from rdflib import URIRef, BNode, Literal, Namespace, Graph, XSD
from rdflib.namespace import RDF, RDFS, DCTERMS, OWL
import json
import re
import sys
import os
import csv
import pandas as pd
from collections import OrderedDict, defaultdict

g = Graph()
ontology = "https://graffiti.data.dice-research.org/ontology/"
resourse = "https://graffiti.data.dice-research.org/resource/"
# ndice = Namespace(resourse)
schema = Namespace("http://schema.org/")
vcard = Namespace("http://www.w3.org/2006/vcard/ns#")
bibtex = Namespace("http://purl.org/net/nknouf/ns/bibtex#") 
swc = Namespace("http://data.semanticweb.org/ns/swc/ontology#")
prov = Namespace("http://www.w3.org/ns/prov#")
nif = Namespace("http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#")
its = Namespace("http://www.w3.org/2005/11/its/rdf#")
sdo = Namespace("http://salt.semanticauthoring.org/ontologies/sdo#")
bibo = Namespace("http://purl.org/ontology/bibo/")
fabio = Namespace("http://purl.org/spar/fabio/")
cvdo = Namespace("https://graffiti.data.dice-research.org/ontology/")
ndice = Namespace("https://graffiti.data.dice-research.org/resource/") #cvdr
graffiti = Namespace("https://graffiti.data.dice-research.org/graffiti#")
FOAF = Namespace('http://xmlns.com/foaf/0.1/')

def handleFile(filename):
    if filename:
        with open(filename, 'r') as f:
            datastore = json.load(f)

    for elem in datastore:
        if "collection" in elem:
            obj = elem["collection"]


            g.namespace_manager.bind("grfr", ndice)
            g.namespace_manager.bind("grfo", cvdo)
            g.namespace_manager.bind("schema", schema)
            g.namespace_manager.bind("dcterms", DCTERMS)
            g.namespace_manager.bind("foaf", FOAF)
            g.namespace_manager.bind("vcard", vcard)
            g.namespace_manager.bind("bibtex", bibtex)
            g.namespace_manager.bind("swc", swc)
            g.namespace_manager.bind("prov", prov)
            g.namespace_manager.bind("nif", nif)
            g.namespace_manager.bind("its", its)
            g.namespace_manager.bind("sdo", sdo)
            g.namespace_manager.bind("bibo", bibo)
            g.namespace_manager.bind("fabio", fabio)
            g.namespace_manager.bind("owl", OWL)

            g.namespace_manager.bind("grfp", graffiti)

            dice = URIRef(resourse+"collection_"+str(obj["_id"]))
            g.add( (dice, RDF.type, cvdo.Collection) )
            g.add( (dice, graffiti.collectionName, Literal(obj["displayname"]["de-DE"],datatype=XSD.string)) )
            g.add( (dice, graffiti.id, Literal(obj["_id"],datatype=XSD.nonNegativeInteger)) )
            g.add( (dice, graffiti.uuid, Literal(obj["uuid"],datatype=XSD.nonNegativeInteger)) )
            g.add( (dice, graffiti.createdDate, Literal(elem["_acl"][0]["date_created"],datatype=XSD.dateTime)) )
    

dirname = sys.argv[1]
num = 0
for filename in os.listdir(dirname):
# handleFile(dirname)
    print(str(num)+"/"+str(len(os.listdir(dirname))))
    handleFile(dirname+"/"+filename)
    num += 1

serilizedRDF = g.serialize(format='turtle')
f = open("rdfCollections.ttl", "w")
f.write(serilizedRDF.decode("utf-8"))
g = Graph()
f.close()
