LOADDIR=`dirname $0`

required_feed=${1:-TRIMET}
db_svr=${2:-"localhost"}
db_port=${3:-"5432"}
ext_data_dir=${4:-"$LOADDIR/../data/shared_stops"}
. $LOADDIR/base.sh


mkdir -p $ext_data_dir

echo "run the shared stops population (run from gtfsdb_ext/ home dir)"
echo "***********************************************************************"
cd $LOADDIR/../

echo " step 1: curl the shared stops mapping between TRIMET and other agencies"
SSCSV="${ext_data_dir}/shared_stops_mapping.csv"
rm -f $SSCSV
curl "https://developer.trimet.org/ws/v3/sharedStops?csv=true&appid=8CBD14D520C6026CC7EEE56A9" > $SSCSV
echo

echo " step 2: load shared stops"
cmd="poetry run update-shared-stops -s ${required_feed} -d $ott_url ${SSCSV}"
echo $cmd
eval $cmd


echo " step 3: shared stops report"
cmd="poetry run shared-stops-report -d $ott_url ${SSCSV} > ${ext_data_dir}/shared_stops.html"
echo $cmd
eval $cmd

echo " step 4: shared stops .csv"
cmd="poetry run shared-stops-csv -d $ott_url ${SSCSV} > ${ext_data_dir}/shared_stops.csv"
echo $cmd
eval $cmd

echo; echo;
