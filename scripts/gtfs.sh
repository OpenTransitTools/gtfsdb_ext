do_load=${1:-"just_echo"}
db_svr=${2:-"localhost"}
db_port=${3:-"5432"}

GDIR=`dirname $0`
. $GDIR/base.sh

gtfs_load="poetry run gtfsdb-load"
install_load=`which gtfsdb-load`
if [ $install_load ]; then
  echo "Will use the installed '$install_load' rather than running via poetry."
  gtfs_load=$install_load
fi

if [ -f "bin/gtfsdb-load" ]; then
  gtfs_load="bin/gtfsdb-load"
fi    

for f in ${GTFS_DIR}/*gtfs.zip
do
  name=$(feed_name_from_zip $f)  
  if [ ${2:-""} == "f" ]; then
    if [ ${name} == "trimet" ] || [ ${name} == "ctran" ]; then
      continue;
    fi
  fi

  cmd="$gtfs_load -c -ct -g -d $ott_url -s ${name} ${f}"
  echo $cmd
  if [ "$do_load" == "load" ]; then
    eval $cmd
  fi
done
