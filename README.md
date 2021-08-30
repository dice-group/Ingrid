# Ingrid

To download json files:
```
python3 download.py
```

To run the generation of the dataset, the following commands are used:
```
python3 jsonToRDF.py folderName/
python3 collectionsToRdf.py folderName/
python3 tagsToRdf.py folderName/
```

folderName/ - the name of the folder that contains json files.

To download taables from wiki:
```
python3 parseHTML.py 'link_to_wiki'
```

To generate rdf from tables:
```
python3 toCrewsInfoRdf.py tables_{now}/
```

## Dataset Image
![alt text](https://github.com/dice-group/Ingrid/blob/main/DatasetImage.jpg?raw=true)



