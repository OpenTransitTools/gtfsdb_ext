SDIR=`dirname $0`
. $SDIR/../base.sh


cmd="poetry run echo-shared-stops -d $ott_url $SDIR/../../ott/gtfsdb/ext/shared_stops/data/shared_stops.csv"
echo $cmd
sleep 2
eval $cmd
