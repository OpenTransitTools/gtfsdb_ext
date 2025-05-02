#
# patch
# changes a GTFS.zip to replace certain files
# November 2024
#
function patch() {
  zip=$1
  file=$2
  url=$3

  cd ~/gtfs/
  echo $PWD
  curl $url > $file
  if [ -f "$zip" ]; then
    zip $zip $file
  else
    echo "$zip does not exist"
  fi
  cd -
}

patch CTRAN_FLEX.gtfs.zip locations.geojson "https://services5.arcgis.com/T6Y1WlK8fKvVXSi3/ArcGIS/rest/services/The_Current_Service_Areas/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=pgeojson"
