##
## crete OTT spatial db for OTT
##
DIR=`dirname $0`
. $DIR/base.sh

## create user and db (default is user='ott', pass='ott' and db='ott' -- see./base.sh)
uu="$psql -d ${def_user} -c \"CREATE USER ${user} WITH PASSWORD '${pass}';\""
dd="$psql -d ${def_user} -c \"CREATE DATABASE ${db} WITH OWNER ${user};\""
ext="$psql -d ${db} -c \"CREATE EXTENSION postgis;\""

for x in "$uu" "$dd" "$ext"
do
  echo $x
  eval $x
done
