VIEWDIR=`dirname $0`


#
# create the SQL (.views files) for the agency aggregate ('current') tables
#
function make_views() {
  gtfs_dir=${1:-"$HOME/gtfs"}
  convert_dir=${2:-"$HOME/rtp/convert"}

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
