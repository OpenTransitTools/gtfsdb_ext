SHPDIR=`dirname $0`
. $SHPDIR/../base.sh

PELIAS=${1:-"pelias@rj-dv-mapgeo01"}
DIR=${2:-"~/gtfs"}

# export pelias .csv file for each feed
for z in ${DIR}/*zip
do 
  f=${z##*/}
  f=${f%.gtfs.zip}
  poetry run pelias-stops -s ${f} "${DIR}/${f}_stops.csv"
done

# move to pelias etl server(s)
for p in $PELIAS
  ssh $p "mkdir -p $DIR"
  scp ${DIR}/*_stops.csv "${p}:$DIR/"
done
