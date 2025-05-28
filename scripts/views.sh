VIEWDIR=`dirname $0`


#
# use the convert tool (https://github.com/OpenTransitTools/convert) to create 'current' schema materizlized .views file
# note: these are aggregate tables (routes/stops/flex/etc..) containing data from all agencies in the region
#
function make_views() {
  local gtfs_dir=${1:-"$HOME/gtfs"}
  local convert_dir=${2:-"$HOME/rtp/convert"}

  cd $convert_dir
  rm -f *.txt
  poetry run gtfs_feeds -sql
  for x in *.txt
  do
    local cmd="mv $x ${gtfs_dir}/${x%%.txt}.views"
    echo $cmd
    eval $cmd
  done
  cd -
}


#
# copy all .views files from this project's data 'customization' folder data/<name>/*.views 
# having the .views checked in here alleviates the need to build these .views files with the 'convert' tool
# note: these are aggregate tables (routes/stops/flex/etc..) containing data from all agencies in the region
#
function copy_views() {
  local gtfs_dir=${1:-"$HOME/gtfs"}
  local agency_dir=${2:-"$VIEWDIR/../data/trimet"}
  local cmd="cp $agency_dir/*.views ${gtfs_dir}/"
  echo $cmd
  eval $cmd
}


function load_views() {
  gtfs_dir=${1:-"$HOME/gtfs"}

  # load any (materialized) views  
  for v in `ls ${gtfs_dir}/*.views`
  do
    echo "load view: $v"
    r="$VIEWDIR/file.sh $v"
    echo $r
    eval $r
    echo
  done
}
