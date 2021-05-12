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

translations = {
    'anmerkungen': 'remarks',
    'bearbeiter': 'editor',
    'fundort_strasse': 'locationStreet',
    'notiz': 'note',
    'fundort_plz': 'postalCode',
    'aufnahmedatum': 'recordingDate',
    'bearbeitungsdatum': 'processingDate',
    'bestand': 'inventory',
    'bildebene': 'imageLayer',
    'buchstabenstil': 'letterStyle',
    'datei': 'file',
    'direktionalitaet': 'directionality',
    'farbe': 'colour',
    'fundort_stadt': 'locationStadt',
    'funktion': 'function',
    'kontext': 'context',
    'motiv': 'motive',
    'oberflaeche': 'surface',
    'sprache': 'language',
    'sprachliche_konstruktion': 'linguisticConstruction',
    'stilelement': 'styleElement',
    'technik': 'technology',
    'thema': 'theme',
    'titel': 'title',
    'traegermedium': 'carrierMedium',
    'typ': 'type',
    'zeichentyp': 'characterType'}

def transalate(word):
    if word in translations:
        word = translations[word]
    return word

def handleFile(filename):
    if filename:
        with open(filename, 'r') as f:
            datastore = json.load(f)

    # sections = ['Abstract', 'Introduction', 'Background',
    #  'RelatedWork', 'Preliminaries', 'Conclusion', 'Experiment', 'Discussion']
    # title = datastore["metadata"]["title"]
    # authors = datastore["metadata"]["authors"]
    # body_text = datastore["body_text"]
    # bib_entries = datastore["bib_entries"]
    objects = datastore["objects"]


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

    exclusions = set(['_id_parent', '_pool', ':inner', ':inner:all', 'taetigkeitszeitraum'])

    for obj in objects:
        # print(obj)
        # dice = URIRef(resourse+str(obj["_system_object_id"]))
        dice = URIRef(resourse+str(obj["graffiti_sprayercrew"]["name"]))
        if 'graffiti_sprayercrew' in obj:
            graffitiInfo = obj['graffiti_sprayercrew']
            # for grkey, value in graffitiInfo.items():
            g.add( (dice, RDF.type, cvdo.CrewMember) )

            

            # print(graffitiInfo.keys())
            keys = graffitiInfo.keys()
            for k in keys:
                if "_nested" in k:
                    if k in graffitiInfo:
                        for subObj in graffitiInfo[k][0].keys():
                            if '_standard' in str(graffitiInfo[k]):
                                textGraffiti = graffitiInfo[k][0][subObj]['_standard']['1']['text']['de-DE']
                            else:
                                textGraffiti = graffitiInfo[k][0][subObj]
                            subObj = transalate(subObj)
                            if subObj == 'colour':
                                subObj = 'hasColour'
                            g.add( (dice, graffiti[subObj], Literal(textGraffiti,datatype=XSD.string)) )
                else: 
                    # print(k)
                    if '_standard' in str(graffitiInfo[k]):
                        textGraffiti = graffitiInfo[k]['_standard']['1']['text']['de-DE']
                        k = transalate(k)
                        if k == 'inventory':
                            k = 'inInventory'
                        g.add( (dice, graffiti[k], Literal(textGraffiti,datatype=XSD.string)) )
                    else:
                        textGraffiti = graffitiInfo[k]
                        if k == '_id' or k == '_version':
                            datatype = XSD.nonNegativeInteger
                        else:
                            if k == 'taetigkeitszeitraum':
                                datatype = XSD.date
                                print(textGraffiti)
                                textGraffitiFrom = textGraffiti['from']
                                k1 = k + 'From'
                                g.add( (dice, graffiti[k1], Literal(textGraffitiFrom,datatype=datatype)) )
                                textGraffitiTo = textGraffiti['to']
                                k2 = k + 'To'
                                g.add( (dice, graffiti[k2], Literal(textGraffitiTo,datatype=datatype)) )
                            else:  
                                if k == 'originalfoto':
                                    datatype = XSD.boolean
                                else:  
                                    datatype = XSD.string
                        if k not in exclusions:
                            k = transalate(k)
                            if k == 'locationStadt':
                                state = textGraffiti.split(',')[0]
                                g.add( (dice, graffiti.hasLocation, ndice[state]) )
                                g.add( (ndice[state], RDF.type, cvdo.State) )
                                g.add( (ndice[state], RDFS.label, Literal(textGraffiti,datatype=datatype)) )
                            else:
                                # datei
                                if k == 'file':
                                    # print(textGraffiti)
                                    versions = textGraffiti[0]['versions']
                                    for v in versions:
                                        print(v)
                                        if v == 'preview_watermark':
                                            twoWords = v.split('_')
                                            v1 = twoWords[0].capitalize()+twoWords[1].capitalize()
                                            predicate = 'has'+v1+'File'
                                            imageIdObj = v1+'_'+str(textGraffiti[0]['_id'])
                                        else:
                                            predicate = 'has'+v.capitalize()+'File'
                                            imageIdObj = v.capitalize()+'_'+str(textGraffiti[0]['_id'])
                                        if 'url' in versions[v]:
                                            g.add( (dice, graffiti[predicate], ndice[imageIdObj]) )
                                            g.add( (ndice[imageIdObj], RDF.type, ndice.ImageFile) )
                                            g.add( (ndice[imageIdObj], graffiti.hasUri, URIRef(versions[v]['url'])) )
                                            g.add( (ndice[imageIdObj], schema.width, Literal(versions[v]['width'],datatype=XSD.nonNegativeInteger)) )
                                            g.add( (ndice[imageIdObj], schema.height, Literal(versions[v]['height'],datatype=XSD.nonNegativeInteger)) )
                                            g.add( (ndice[imageIdObj], graffiti.extension, Literal(versions[v]['extension'],datatype=XSD.string)) )
                                            g.add( (ndice[imageIdObj], graffiti.aspect_ratio, Literal(versions[v]['aspect_ratio'],datatype=XSD.float)) )

                                else:
                                    k = k.replace('_', '')
                                    if k == 'text':
                                        k = 'hasText'
                                    g.add( (dice, graffiti[k], Literal(textGraffiti,datatype=datatype)) )

 

    # schema.author


    
    # # sameAs linking
    # if pmcid:
    #     g.add( (dice, OWL.sameAs, URIRef("http://ns.inria.fr/covid19/"+pmcid)) )
    #     g.add( (dice, OWL.sameAs, URIRef("https://www.ncbi.nlm.nih.gov/pmc/articles/"+pmcid)) )
    # if sha:
    #     g.add( (dice, OWL.sameAs, URIRef("http://ns.inria.fr/covid19/"+sha)) )    
    #     g.add( (dice, OWL.sameAs, URIRef("http://pubannotation.org/docs/sourcedb/CORD-19/sourceid/"+sha)) )
    #     g.add( (dice, OWL.sameAs, URIRef("https://data.linkeddatafragments.org/covid19?object=http%3A%2F%2Fidlab.github.io%2Fcovid19%23"+sha)) )
    #     g.add( (dice, OWL.sameAs, URIRef("https://fhircat.org/cord-19/fhir/PMC/Composition/"+sha+".ttl")) )
    #     g.add( (dice, RDFS.seeAlso, URIRef("https://fhircat.org/cord-19/fhir/PMC/Composition/"+sha+".json")) )


    # # the provenance
    # g.add( (dice, prov.hadPrimarySource, ndice.cord19Dataset) )
    # g.add( (ndice.cord19Dataset, RDF.type, prov.Entity) )
    # g.add( (ndice.cord19Dataset, prov.generatedAtTime, Literal("2020-05-21T02:52:02Z",datatype=XSD.dateTime)) )
    # g.add( (ndice.cord19Dataset, prov.wasDerivedFrom, Literal("https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/latest/document_parses.tar.gz",datatype=XSD.string)) )
  
    #
        # if title:
        #     g.add( (dice, DCTERMS.title, Literal(title.strip().replace("\n",""),datatype=XSD.string)) )
        # g.add( (dice, RDF.type, swc.Paper) )
        # g.add( (dice, RDF.type, fabio.ResearchPaper) )
        # g.add( (dice, RDF.type, bibo.AcademicArticle) )
        # g.add( (dice, RDF.type, schema.ScholarlyArticle) )
        # addAuthors(authors, dice)

# dirname = sys.argv[1]
# handleFile(dirname)

handleFile('spayercrews145633-145740@16184ddb-0cf4-44cf-a00e-d6800d28c027.json')

serilizedRDF = g.serialize(format='turtle')
f = open("spayercrews_v2.ttl", "w")
f.write(serilizedRDF.decode("utf-8"))
g = Graph()
