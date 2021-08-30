#!/bin/bash
python3 download.py

stringVersion=jsonFiles_
now="$(date +'%Y-%m-%d')"
folderName=$stringVersion$now

python3 jsonToRdf.py $folderName/
python3 collectionsToRdf.py $folderName/
python3 tagsToRdf.py $folderName/

fileName=rdfGraffiti_
cp rdfGraffiti.ttl "${fileName}${now}.ttl"
cp rdfGraffiti.ttl /home/user/Documents/graffiti/rdf/rdfGraffiti.ttl

fileName=tags_
cp rdfTags.ttl "${fileName}${now}.ttl"
cp rdfTags.ttl /home/user/Documents/graffiti/rdf/rdfTags.ttl

fileName=collections_
cp rdfCollections.ttl "${fileName}${now}.ttl"
cp rdfCollections.ttl /home/user/Documents/graffiti/rdf/rdfCollections.ttl

################################

# cd crewsInfoToRdf
# # download data from wiki
# python3 parseHTML.py 'https://wikis.uni-paderborn.de/graffiti/Information_zu_den_Namen_(Pseudonymen)'
# # generate rdf from tables
# python3 toCrewsInfoRdf.py tables_${now}/

# python3 parseHTML.py 'https://wikis.uni-paderborn.de/graffiti/Symbole_und_Ideogramme'
# python3 parseHTML.py 'https://wikis.uni-paderborn.de/graffiti/Anmerkungsfeld'

# cd..

################################
# # Update in virtuoso

# instead of stopping current virtuoso and removing database, we can copy the db and remove the graph with sql query, otherwise the auth is removed as well
# move old database
db=db_
fn=$db$now
mkdir $fn
cp /home/user/Documents/vos19/database/virtuoso.db "${fn}/virtuoso.db"

source DBA_PASSWORD

# remove old graph
sleep 2m
docker exec -it INGRID bash -c "cd /opt/virtuoso-opensource/bin && ./isql 1111 dba $PASS < /rdfData/remove_graph.sql"

# upload new files
sleep 2m
docker exec -it INGRID bash -c "cd /opt/virtuoso-opensource/bin && ./isql 1111 dba $PASS < /rdfData/add.sql"