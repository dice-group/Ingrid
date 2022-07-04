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
graffiti = Namespace("https://graffiti.data.dice-research.org/graffiti/")
FOAF = Namespace('http://xmlns.com/foaf/0.1/')


def handleFile():


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


    # metadata

    dice = None

    for row in reader:
        longitude = None
        latitude = None
        for heading in row:
            heading = str(heading)

            # strName = str(row['iso3'].split(',')[0].strip())
            # strName = str(row['highwayThing'].split("triplify/")[1])
            # snakecase to lowerCamelCase
            # strCamelCase = re.sub(r"_(\w)", repl, strName)
            # print(strName)

            dice = URIRef(row['highwayThing'])

            # headingLower = heading.lower().replace(' ', '')
            strCamelCase = re.sub(r"_(\w)", repl, heading)
            metapredicate = graffiti[strCamelCase]
            preprocessedValue = row[heading].replace("'",'')
            metaobject = Literal(preprocessedValue,datatype=XSD.string)

            
            if row[heading] != "":
                g.add( (dice, RDF.type, cvdo.Street) )
                g.add( (dice, metapredicate, metaobject) )

    print('CSV has finished')

reader = pd.read_csv('streetNamesOfPaderborn.csv', keep_default_na=False).to_dict('records', into=OrderedDict)

def isnan(value):
    try:
        import math
        return math.isnan(float(value))
    except:
        return False

def repl(m):
    return m.group(1).upper()

def capitalizeWords(s):
  return re.sub(r'\w+', lambda m:m.group(0).capitalize(), s).replace(" ", "")


handleFile()

serilizedRDF = g.serialize(format='turtle')
f = open("streetsOfPaderborn.ttl", "w", encoding='utf-8')
f.write(serilizedRDF)
g = Graph()