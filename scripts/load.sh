##
## load gtfsdb spatial db for OTT
## *note*: requires the ott db to exist 
##
LOADDIR=`dirname $0`
. $LOADDIR/base.sh
. $LOADDIR/shapes.sh
. $LOADDIR/schemas.sh
. $LOADDIR/views.sh

required_feed=${1:-TRIMET}
ext_data_dir="${LOADDIR}/../data/${required_feed,,}"
mkdir -p $ext_data_dir

chk=${GTFS_DIR}/${required_feed}.gtfs.zip
if [ -f $chk ]; then
  echo "INFO: starting the load as file $chk *does* exist."

  echo "step 0: remove old .sql files from gtfs dir"
  echo "*******************************************"
  rm -f ${GTFS_DIR}/*.sql ${GTFS_DIR}/*schema ${GTFS_DIR}/*views

  echo "step 1: patch CTRAN_FLEX, etc..."
  echo "********************************"
  $LOADDIR/patch_gtfs.sh

  echo "step 2: create 'current' schema (in addition to gtfs agency schemas)"
  echo "********************************************************************"
  make_schema "current"
  load_schemas

  echo "step 3: grab and load the shape (.sql) files, ala the trimet rail dashed-lines"
  echo "******************************************************************************"
  get_shps
  load_shps

  echo "step 4: load gtfs feeds into gtfsdb (run from gtfsdb_ext/ home dir)"
  echo "*******************************************************************"
  cd $LOADDIR/../
  for f in ${GTFS_DIR}/*gtfs.zip
  do
    name=$(feed_name_from_zip $f)
    CURRENT_FLAG="-cta"
    if [ ${name} == "trimet" ] || [ ${name} == "other-agency-here" ]; then
      CURRENT_FLAG="-ct"  # actually use date to calculate current views
    fi
    cmd="poetry run gtfsdb-load -c ${CURRENT_FLAG} -g -d $ott_url -s ${name} ${f}"
    echo "  $cmd"
    eval $cmd
    sleep 1
  done
  cd -
  echo; echo;

  echo "step 5: run the shared stops population (run from gtfsdb_ext/ home dir)"
  echo "***********************************************************************"
  cd $LOADDIR/../

  echo " step 5a: curl the shared stops"
  SSCSV="${ext_data_dir}/shared_stops.csv"
  rm -f $SSCSV
  curl "https://developer.trimet.org/ws/v3/sharedStops?csv=true&appid=8CBD14D520C6026CC7EEE56A9" > $SSCSV
  echo

  echo " step 5b: load / update shared stops"
  cmd="poetry run update-shared-stops -s ${required_feed} -d $ott_url ${SSCSV}"
  echo $cmd
  eval $cmd
  cd -
  echo; echo;

  echo "step 6: export the agency data for deploy to other servers"
  echo "**********************************************************"
  for f in ${GTFS_DIR}/*gtfs.zip
  do
    name=$(feed_name_from_zip $f)
    dump="$pg_dump $db -n ${name} > ${GTFS_DIR}/${name}.sql"
    echo $dump
    eval $dump
  done
  echo; echo;

  echo "step 7: create the 'current' views, etc..."
  echo "  NOTE: we need views to run after shared-stops, as we then exclude shared stops"
  echo "**********************************************************"
  make_views ${GTFS_DIR} ${ext_data_dir}
  copy_views ${GTFS_DIR} ${ext_data_dir}
  load_views
  echo;  echo;
else
  echo "WARN: not loading as file $chk *does not* exist."
fi
