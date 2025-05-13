#
# current routes/stops/etc... load gtfsdb
#
do_load=${1:-"just_echo"}
db_svr=${2:-"localhost"}
db_port=${3:-"5432"}

CURDIR=`dirname $0`
. $CURDIR/base.sh

gtfsdb_current="poetry run gtfsdb-current-load"
install_load=`which gtfsdb-current-load`
if [ $install_load ]; then
  gtfsdb_current=$install_load
fi

for f in ${GTFS_DIR}/*sql*
do
  name=$(feed_name_from_zip $f)  

  cmd="$gtfsdb_current -g -d $ott_url -s ${name} ${f}"
  echo $cmd
  if [ "$do_load" == "load" ]; then
    eval $cmd
  fi
done

for v in ${GTFS_DIR}/*.views
do
  if [ "$db_svr" == "localhost" ]; then
    cmd="$CURDIR/file.sh $v"
  else
    cmd="ssh $db_svr $HOME/geo/scripts/db/file.sh ${v}*"
  fi
  echo "$cmd"
  if [ "$do_load" == "load" ]; then
    eval $cmd
  fi
done


if [ "$do_load" == "load" ]; then
  echo "!!!! TODO: remove geoserver cache  on $db_svr !!!!"
  echo "???? TODO - what other cache / junk needs to be purged weekly on the current update ????"
fi
