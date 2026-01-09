SDIR=`dirname $0`
. $SDIR/../base.sh

ext_data_dir=data/shared_stops
mkdir -p ${ext_data_dir}
echo $ott_url

echo " step a: curl the shared stops"
SSCSV="${ext_data_dir}/shared_stops.csv"
rm -f $SSCSV
curl "https://developer.trimet.org/ws/v3/sharedStops?csv=true&appid=8CBD14D520C6026CC7EEE56A9" > $SSCSV
echo

echo " step b: shared stops report"
cmd="poetry run shared-stops-report -d $ott_url ${SSCSV} > ${ext_data_dir}/shared_stops.html 2> /dev/null"
echo $cmd
eval $cmd
echo

echo " step c: more the shared stops"
cmd="poetry run echo-shared-stops -d $ott_url ${SSCSV} > ${ext_data_dir}/shared_stops.txt 2> /dev/null"
echo $cmd
eval $cmd
more "${ext_data_dir}/shared_stops.txt"
