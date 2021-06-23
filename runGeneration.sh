#!/bin/bash
python3 download.py

stringVersion=jsonFiles_
now="$(date +'%Y-%m-%d')"
folderName=$stringVersion$now

python3 jsonToRdf.py $folderName/

fileName=rdfGraffiti_
filenow=.ttl
cp rdfGraffiti.ttl $fileName$now$filenow
cp rdfGraffiti.ttl /home/user/Documents/graffiti/rdf/rdfGraffiti.ttl

################################
# # Update in virtuoso

# copy sql queries file into folder with rdfs
cp add.sql /home/user/Documents/graffiti/rdf/add.sql

# stop current virtuoso docker
docker stop INGRID

# move old database
db=db_
fn=$db$now
mkdir $fn
mv /home/user/Documents/vos19/database/virtuoso.db $fn
rm -rf /home/user/Documents/vos19/database/virtuoso.trx
rm -rf /home/user/Documents/vos19/database/virtuoso.log
rm -rf /home/user/Documents/vos19/database/virtuoso-temp.db
rm -rf /home/user/Documents/vos19/database/virtuoso.pxa
# run new virtuoso
source DBA_PASSWORD
docker run -d=true --rm --name INGRID -e DBA_PASSWORD=$PASS -it -v /home/user/Documents/vos19/database:/database -v /home/user/Documents/graffiti/rdf:/rdfData -t -p 1111:1111 -p 8890:8890 -i openlink/virtuoso-opensource-7

# upload new files
sleep 2m
docker exec -it INGRID bash -c "cd /opt/virtuoso-opensource/bin && ./isql 1111 dba $PASS < /rdfData/add.sql"