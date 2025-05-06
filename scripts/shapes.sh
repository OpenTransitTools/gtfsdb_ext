SHPDIR=`dirname $0`
. $SHPDIR/base.sh

SHPS="rail.sql" 


function get_shps() {
  for f in $SHPS
  do
    cmd="curl http://maps6.trimet.org/data/$f > $GTFS_DIR/$f"
    echo $cmd
    eval $cmd
  done
}


function load_shps() {
  for f in $SHPS
  do
    cmd="$SHPDIR/file.sh $GTFS_DIR/$f"
    echo "shp load: $cmd"
    eval $cmd
  done
}
