SHPDIR=`dirname $0`
. $SHPDIR/../base.sh

SCP=${1:-""}
DIR=${2:-"${HOME}/gtfs"}

# export stops .csv for each feed (pelias format)
for z in `ls ${DIR}/*zip`
do 
  f=${z##*/}
  f=${f%.gtfs.zip}
  cmd="poetry run pelias-stops -s ${f} \"${DIR}/${f}_stops.csv\""
  echo $cmd
  eval $cmd
done

cmd="poetry run pelias-pr > \"${DIR}/pr.csv\""
echo $cmd
eval $cmd

if [ $SCP ]; then
  cmd="scp -q ${DIR}/*.csv $SCP:~/gtfs/"
  echo $cmd
  eval $cmd
fi
