GEODIR=`dirname $0`
. $GEODIR/../base.sh
. $GEODIR/../shapes.sh
. $GEODIR/../schemas.sh
. $GEODIR/../views.sh

GTFS_DIR=${1:-"${HOME}/gtfs"}
EXT_DATA_DIR=${2:-"${GEODIR}/../../data/trimet"}

echo "step 1: export the agency data for deploy to other servers"
echo "**********************************************************"
for f in ${GTFS_DIR}/*gtfs.zip
do
  name=$(feed_name_from_zip $f)
  dump="$pg_dump $db -n ${name} > ${GTFS_DIR}/${name}.sql"
  echo $dump
  #eval $dump
done
echo; echo;


echo "step 2: create the 'current' views, etc..."
echo "  NOTE: we need views to run after shared-stops, as we then exclude shared stops"
echo "**********************************************************"
get_shps
make_schema "current"
make_views ${GTFS_DIR} ${EXT_DATA_DIR}
copy_views ${GTFS_DIR} ${EXT_DATA_DIR}
echo;  echo;
