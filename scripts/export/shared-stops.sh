SDIR=`dirname $0`
. $SDIR/../base.sh

CSV=ss.csv
rm -f $CSV
curl "https://developer.trimet.org/ws/v3/sharedStops?csv=true&appid=8CBD14D520C6026CC7EEE56A9" > $CSV

# test data (don't rm -f $CSV above):
#CSV=${1:-"$SDIR/../../ott/gtfsdb/ext/shared_stops/data/shared_stops.csv"}

cmd="poetry run echo-shared-stops -d $ott_url $CSV"
echo $cmd
sleep 2
eval $cmd
