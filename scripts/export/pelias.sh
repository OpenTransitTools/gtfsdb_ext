SHPDIR=`dirname $0`
. $SHPDIR/../base.sh

PELIAS=${1:-"pelias@rj-dv-mapgeo01"}
DIR=${2:-"~/gtfs"}

# export pelias .csv file for each feed
for z in ~/gtfs/*zip
do 
  f=${z##*/}
  f=${f%.gtfs.zip}
  #poetry run pelias-stops -s ${f} "${f}_stops.csv"
done

# move to pelias etl server
ssh $PELIAS "mkdir -p $DIR"
scp *_stops.csv "${PELIAS}:$DIR"
mv *_stops.csv ~/gtfs/
