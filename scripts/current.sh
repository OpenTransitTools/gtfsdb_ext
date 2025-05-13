##
## load gtfsdb spatial db for OTT
## *note*: requires the ott db to exist 
##
LDDIR=`dirname $0`
. $LDDIR/base.sh

gtfsdb_current="poetry run gtfsdb-current-load"

for f in ${GTFS_DIR}/*sql*
do
  name=$(feed_name_from_zip $f)  

  cmd="$gtfsdb_current -g -d $ott_url -s ${name} ${f}"
  echo $cmd
  eval $cmd
done

for v in ${GTFS_DIR}/*.views
do
  cmd="$LDDIR/file.sh $v"
  echo $cmd
  eval $cmd
done
