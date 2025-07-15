SHPDIR=`dirname $0`
. $SHPDIR/../base.sh

PELIAS=${1:-"pelias@rj-st-mapgeo01"}

# export pelias .csv file for each feed
for z in ~/gtfs/*zip
do 
  f=${z##*/}
  f=${f%.gtfs.zip}
  poetry run pelias-stops -s ${f} "${f}_stops.csv"
done

# move to pelias etl server
scp *_stops.csv "${PELIAS}:~/gtfs/"
