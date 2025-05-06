##
## drop OTT database
##
DIR=`dirname $0`
. $DIR/base.sh

dropdb="$psql -d ${def_user} -c \"DROP DATABASE ${db};\""
echo $dropdb
eval $dropdb

$psql -d ${def_user} -c "DROP USER ${user};"
