from rdflib import URIRef, BNode, Literal, Namespace, Graph, XSD
from rdflib.namespace import RDF, RDFS, DCTERMS, OWL
import json
import re
import os
import sys

g = Graph()
ontology = "https://graffiti.data.dice-research.org/ontology/"
resource = "https://graffiti.data.dice-research.org/resource/"
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

translations = {
	'anmerkungen': 'hasRemarks',
	'bearbeiter': 'editor',
	'fundort_strasse': 'hasLocationStreet',
	'notiz': 'hasNote',
	'fundort_plz': 'hasPostalCode',
	'aufnahmedatum': 'hasRecordingDate',
	'bearbeitungsdatum': 'hasProcessingDate',
	'bestand': 'inInventory',
	'bildebene': 'hasImageLayer',
	'buchstabenstil': 'hasLetterStyle',
	'datei': 'file',
	'direktionalitaet': 'hasDirectionality',
	'farbe': 'hasColour',
	'fundort_stadt': 'locationStadt',
	'funktion': 'hasFunction',
	'kontext': 'hasContext',
	'motiv': 'hasMotive',
	'oberflaeche': 'hasSurface',
	'sprache': 'hasLanguage',
	'sprachliche_konstruktion': 'hasLinguisticConstruction',
	'stilelement': 'hasSyleElement',
	'technik': 'hasTechnology',
	'thema': 'hasTheme',
	'titel': 'hasTitle',
	'traegermedium': 'hasCarrierMedium',
	'typ': 'hasType',
	'zeichentyp': 'hasCharacterType',
	'eingebettetesgraffiti': 'hasEmbeddedGraffiti',
	'enthaltene_sprachliche_konstruktion': 'hasLinguisticConstruction',
	'redakteur': 'editor',
	'bearbeitungsstand': 'hasProcessingStatus',
	'id': 'hasId',
	'version': 'hasVersion',
	'architektur': 'hasArchitecture',
	'datierung': 'hasDate',
	'literatur': 'hasLiterature',
	'figurenstil': 'hasFigureStyle',
	'sixomcid': 'hasSixomcid',
	'sixomcuid': 'hasSixomcuid',
	'fundortgps': 'hasFundortGPS'
}


def translate(word):
	if word in translations:
		word = translations[word]
	return word


def handleFile(filename):
	if filename:
		with open(filename, 'r', encoding="utf8") as f:
			datastore = json.load(f)

	# sections = ['Abstract', 'Introduction', 'Background',
	#  'RelatedWork', 'Preliminaries', 'Conclusion', 'Experiment', 'Discussion']
	# title = datastore["metadata"]["title"]
	# authors = datastore["metadata"]["authors"]
	# body_text = datastore["body_text"]
	# bib_entries = datastore["bib_entries"]
	if "objects" in datastore:
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

		exclusions = set(['_id_parent', '_pool', ':inner', ':inner:all'])

		for obj in objects:
			dice = URIRef(resource + str(obj["_system_object_id"]))
			if '_collections' in obj and len(obj['_collections']):
				# print(obj['_collections'])
				collections = obj['_collections']
				for collection in collections:
					if "_id" in collection:
						g.add( (dice, graffiti.hasCollectionId, ndice["collection_"+str(collection['_id'])] ))
			if '_last_modified' in obj:
				g.add( (dice, graffiti.lastModified, Literal(obj['_last_modified'],datatype=XSD.dateTime)) )
			if '_created' in obj:
				g.add( (dice, graffiti.creationDate, Literal(obj['_created'],datatype=XSD.dateTime)) )
			if '_tags' in obj:
				tags = obj['_tags']
				for tag in tags:
					if "_id" in tag:
						g.add( (dice, graffiti.hasTagId, ndice["tag_"+str(tag['_id'])] ))
					if "name" in tag:
						tagName = tag['_name']['de-DE']
						g.add( (dice, graffiti.hasTagName,  Literal(tagName,datatype=XSD.string)) )
			if 'graffiti' in obj:
				graffitiInfo = obj['graffiti']
				# for grkey, value in graffitiInfo.items():
				g.add((dice, RDF.type, cvdo.Graffiti))

				# print(graffitiInfo.keys())
				keys = graffitiInfo.keys()
				for k in keys:
					if "_nested" in k:
						if k in graffitiInfo:
							if len(graffitiInfo[k]) != 0:
								for elem in graffitiInfo[k]:
									for subObj in elem.keys():
										textGraffiti = elem[subObj]['_standard']['1']['text']['de-DE']
										subObj = translate(subObj)
										if subObj == 'sprayercrew':
											g.add((dice, RDFS.label, Literal(textGraffiti, datatype=XSD.string)))
										else:
											g.add((dice, graffiti[subObj], Literal(textGraffiti, datatype=XSD.string)))
					else: 
						# print(k)
						if '_standard' in str(graffitiInfo[k]):
							textGraffiti = graffitiInfo[k]['_standard']['1']['text']['de-DE']
							k = translate(k)
							if not 'has' in k and not 'in' in k:
								print(k)
							g.add((dice, graffiti[k], Literal(textGraffiti,datatype=XSD.string)))
						else:
							textGraffiti = graffitiInfo[k]
							if k == '_id' or k == '_version':
								datatype = XSD.nonNegativeInteger
							else:
								if k == 'aufnahmedatum' or k == 'bearbeitungsdatum':
									datatype = XSD.date
									textGraffiti = textGraffiti['value']
								else:  
									if k == 'originalfoto':
										k = 'hasOriginalPhoto'
										datatype = XSD.boolean
									else:  
										datatype = XSD.string
							if k not in exclusions:
								k = translate(k)
								if k == 'locationStadt':
									city = textGraffiti.split(',')[0].strip().replace(" ", "")
									g.add((dice, graffiti.hasLocation, ndice[city]))
									g.add((ndice[city], RDF.type, cvdo.City))
									g.add((ndice[city], RDFS.label, Literal(textGraffiti, datatype=datatype)))
								else:
									if k == 'editor':
										name_arr = textGraffiti.split(";")
										for annotator in name_arr:
											annotator = annotator.strip()
											anno_resource = annotator.replace(" ", "")
											g.add((dice, graffiti.hasAnnotator, ndice[anno_resource]))
											g.add((ndice[anno_resource], RDF.type, FOAF.Person))
											names = annotator.split(" ")
											if len(names) == 2:
												g.add((ndice[anno_resource], FOAF.firstName, Literal(names[0], datatype=datatype)))
												g.add((ndice[anno_resource], FOAF.lastName, Literal(names[1], datatype=datatype)))
											else:
												g.add((ndice[anno_resource], FOAF.givenName, Literal(names[0], datatype=datatype)))
									if k == 'spruehercrew':
										crewArr = textGraffiti.split('|')
										for crew in crewArr:
											crewName = re.sub(r'"|„|“|\?|<|\`| ', '', crew).upper().strip()
											originalCrewName = re.sub(r'"|\?|„|“', '', crew).strip()
											if(originalCrewName != ""):
												g.add( (dice, graffiti.hasGraffitiSprayerCrew, ndice[crewName]) )
												g.add( (ndice[crewName], RDF.type, cvdo.GraffitiSprayerCrew) )
												g.add( (ndice[crewName], RDFS.label, Literal(originalCrewName,datatype=datatype)) )
									# datei
									if k == 'file':
										# print(textGraffiti)
										versions = textGraffiti[0]['versions']
										for v in versions:
											# print(v)
											if v == 'preview_watermark':
												twoWords = v.split('_')
												v1 = twoWords[0].capitalize()+twoWords[1].capitalize()
												predicate = 'has'+v1+'File'
												imageIdObj = v1+'_'+str(textGraffiti[0]['_id'])
											else:
												predicate = 'has'+v.capitalize()+'File'
												imageIdObj = v.capitalize()+'_'+str(textGraffiti[0]['_id'])
											if 'url' in versions[v]:
												g.add((dice, graffiti[predicate], ndice[imageIdObj]))
												g.add((ndice[imageIdObj], RDF.type, cvdo.ImageFile))
												g.add((ndice[imageIdObj], graffiti.hasUri, URIRef(versions[v]['url'])))
												g.add((ndice[imageIdObj], schema.width, Literal(versions[v]['width'],datatype=XSD.nonNegativeInteger)))
												g.add((ndice[imageIdObj], schema.height, Literal(versions[v]['height'],datatype=XSD.nonNegativeInteger)))
												g.add((ndice[imageIdObj], graffiti.hasExtension, Literal(versions[v]['extension'],datatype=XSD.string)))
												if 'aspect_ratio' in versions[v]:
													g.add((ndice[imageIdObj], graffiti.hasAspectRatio, Literal(versions[v]['aspect_ratio'],datatype=XSD.float)))

									else:
										k = k.replace('_', '')
										if k == 'text':
											# k = 'hasText'
											symbols = re.findall('\{[A-Z]*\}', textGraffiti, re.IGNORECASE)
											if symbols:
												# print(symbols)item
												for symbol in symbols:
													g.add( (dice, graffiti.hasGraffitiSymbol, ndice["symbol_"+symbol.replace("{","").replace("}","").upper()]) )
										if k != 'editor' and k != 'spruehercrew':
											if k == 'text' or k == 'item':
												if '_nested:graffiti__sprachen' in graffitiInfo:
													langFromGraffiti = graffitiInfo['_nested:graffiti__sprachen'][0]['sprache']['_standard']['1']['text']['de-DE']
													if '-' in langFromGraffiti:
														lang = langFromGraffiti.split('-')[0].strip()
														if k == 'text':
															g.add((dice, graffiti.hasText, Literal(textGraffiti,lang=lang)))
														if k == 'item':
															g.add((dice, graffiti.hasItem, Literal(textGraffiti,lang=lang)))

											else:
												k = translate(k)
												if 'has' not in k and 'in' not in k:
													print(k)
												g.add((dice, graffiti[k], Literal(textGraffiti,datatype=datatype)))


dirname = sys.argv[1]
num = 0
for filename in os.listdir(dirname):
	print(str(num)+"/"+str(len(os.listdir(dirname))))
	handleFile(dirname+"/"+filename)
	num += 1
serializedRDF = g.serialize(format='turtle')
f = open("rdfGraffiti.ttl", "w", encoding='utf8')
f.write(serializedRDF)
g = Graph()
f.close()