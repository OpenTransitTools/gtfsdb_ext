#
# patch
# changes a GTFS.zip to replace certain files
# November 2024
#
function patch() {
  local zip=$1
  local file=$2
  local url=$3
  local bkup=$4
  local exp_size=${5:-100000}

  cd ~/gtfs/
  echo $PWD
  curl $url > $file
  local size=`ls -ltr $file | awk -F" " '{ print $5 }'`
  if [ $size -lt $exp_size ]; then
    if [ -f "$bkup" ]; then
      echo
      echo "WARN: $url download of $file is only $size bytes in size ... patching $zip with $bkup"
      echo
      cp $bkup $file
    else
      echo
      echo "ERROR: $url download of $file is only $size bytes in size ... not patching $zip"
      echo
      rm $file
    fi
  fi

  if [ -f "$file" ] && [ -f "$zip" ]; then
    zip $zip $file
  else
    echo
    echo "$file and/or $zip does not exist .. not patching the .zip"
    echo
  fi
  cd -
}

patch CTRAN_FLEX.gtfs.zip locations.geojson "https://services5.arcgis.com/T6Y1WlK8fKvVXSi3/ArcGIS/rest/services/The_Current_Service_Areas/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=pgeojson" ~/OLD/ctran-flex-june-2025.geojson
