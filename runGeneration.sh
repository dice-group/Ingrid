#!/bin/bash
python3 download.py

stringVersion=jsonFiles_
now="$(date +'%Y-%m-%d')"
folderName=$stringVersion$now

python3 jsonToRdf.py $folderName/

fileName=rdfGraffiti_
cp rdfGraffiti.ttl "${fileName}${now}.ttl"
cp rdfGraffiti.ttl /home/user/Documents/graffiti/rdf/rdfGraffiti.ttl

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