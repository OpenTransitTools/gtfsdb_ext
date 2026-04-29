##
## crete OTT spatial db for OTT
##
DIR=`dirname $0`
. $DIR/base.sh


## create user and db (default is user='ott', pass='ott' and db='ott' -- see./base.sh)
cmd="$psql -d ${def_user} -c \"CREATE USER ${user} WITH PASSWORD '${pass}';\""
echo $cmd
eval $cmd


# create ott DB (and other needed dbs)
for d in $db logs
do
  cmd="$psql -c \"CREATE DATABASE ${d} WITH OWNER ${user};\""
  echo $cmd
  eval $cmd

  cmd="$psql $d -c \"CREATE EXTENSION postgis;\""
  echo $cmd
  eval $cmd
done


# final create misc db junk (schemas, etc...)
sl="$psql -d logs -c \"CREATE SCHEMA logs AUTHORIZATION ${user};\""
for cmd in "$sl"
do
  echo $cmd
  eval $cmd
done
