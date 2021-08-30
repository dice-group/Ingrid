from rdflib import URIRef, BNode, Literal, Namespace, Graph, XSD
from rdflib.namespace import RDF, RDFS, DCTERMS, OWL
import json
import re
import sys
import os
import csv
import pandas as pd
from collections import OrderedDict, defaultdict
import pyreadr
import pycountry
import urllib.parse

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
graffiti = Namespace("https://graffiti.data.dice-research.org/graffiti#")
FOAF = Namespace('http://xmlns.com/foaf/0.1/')


def handleFile(filename):
    if filename:
        reader = pd.read_csv(filename, delimiter="|", keep_default_na=False).to_dict('records', into=OrderedDict)


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
    num = 0
    for row in reader:
        longitude = None
        latitude = None
        for heading in row:
            heading = str(heading)

            # strName = str(row['iso3'].split(',')[0].strip())
            if "Akronym" in row:
                strName = str(row['Akronym']).replace("'",'').replace(' ', '')
                # snakecase to lowerCamelCase
                # strCamelCase = re.sub(r"_(\w)", repl, strName)
                # print(strName)
            if "Zahl" in row:
                strName = str(row['Zahl'])
            if "Sprayername" in row:
                strName = str(row['Sprayername'])
            else:
                strName = 'tableItem'+str(num)
                num = num + 1

            strName = urllib.parse.quote(strName)
            dice = URIRef(ndice+strName)

            headingLower = heading.lower().replace(' ', '')
            strCamelCase = urllib.parse.quote(re.sub(r"_(\w)", repl, headingLower))
            print(strCamelCase)
            metapredicate = graffiti[strCamelCase]
            preprocessedValue = row[heading].replace("'",'')
            metaobject = Literal(preprocessedValue,datatype=XSD.string)

            if heading == 'Bearbeiter':
                annotators = re.split(',|;',preprocessedValue)
                # preprocessedValue.split(',')
                for a in annotators:
                    a = a.strip()
                    a = urllib.parse.quote(a)
                    g.add( (dice, graffiti.annotator, ndice[a]) )
                    g.add( (ndice[a], RDF.type, FOAF.Person) )
                    g.add( (ndice[a], FOAF.givenName, Literal(a,datatype=XSD.string)) )

            if heading == 'Langform':
                longformsOfName = re.split(',',preprocessedValue)
                for n in longformsOfName:
                    n = n.strip()
                    g.add( (dice, graffiti.longForm, Literal(n,datatype=XSD.string)) )

            if heading == 'Mitglieder der Crew':
                if preprocessedValue != '-':
                    longformsOfName = re.split(',',preprocessedValue)
                    for n in longformsOfName:
                        n = n.strip()
                        # g.add( (dice, graffiti.crewMember, Literal(n,datatype=XSD.string)) )
                        res = n.replace(" ","").replace(")","")
                        res = res.split("(")[0]
                        diffLabels = re.split("/|;",res)
                        for dl in diffLabels:
                            if ":" in dl:
                                dl = dl.split(":")[1].replace("?","")
                            r = dl.upper()
                            if r != "":
                                r = urllib.parse.quote(r)
                                g.add( (dice, graffiti.hasCrewMember, ndice[r]) )
                                g.add( (ndice[r], RDF.type, cvdo.CrewMember ))
                                g.add( (ndice[r], RDFS.label, Literal(dl,datatype=XSD.string)) )

            if heading == 'Beleg':
                if preprocessedValue != '-':
                    longformsOfName = re.split(',',preprocessedValue)
                    for n in longformsOfName:
                        n = n.strip()
                        g.add( (dice, graffiti.beleg, Literal(n,datatype=XSD.string)) )

            if heading == 'Akronym':
               metapredicate = graffiti.shortForm

            if heading == 'Anmerkungen':
               metapredicate = graffiti.remarks
            
            if row[heading] != "" and preprocessedValue != '-' and heading != 'Bearbeiter' and heading != 'Langform' and heading != 'Mitglieder der Crew' and heading != 'Beleg':
                g.add( (dice, RDF.type, cvdo.Crew) )
                g.add( (dice, metapredicate, metaobject) )

    print('CSV has finished')

# reader = pd.read_csv('Übersicht Crews.csv', delimiter="|", keep_default_na=False).to_dict('records', into=OrderedDict)

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


# handleFile()

# serilizedRDF = g.serialize(format='turtle')
# f = open("crews_info_v2.ttl", "w")
# f.write(serilizedRDF.decode("utf-8"))
# g = Graph()


dirname = sys.argv[1]
num = 0
for filename in os.listdir(dirname):
# handleFile(dirname)
    print(str(num)+"/"+str(len(os.listdir(dirname))))
    handleFile(dirname+"/"+filename)
    num += 1

serilizedRDF = g.serialize(format='turtle')
f = open("crews_info_test1.ttl", "w")
f.write(serilizedRDF.decode("utf-8"))
g = Graph()
f.close()

