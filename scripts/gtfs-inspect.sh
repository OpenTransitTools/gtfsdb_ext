g1=${1}
g2=${2}
txt=${3:-trips.txt}

if [ -f "$g1" ] && [ -f "$g2" ]; then
  unzip $g1 $txt; mv $txt /tmp/${txt}-1
  unzip $g2 $txt; mv $txt /tmp/${txt}-2
  echo "compare $txt $g1 v. $g2"
  cmd="diff /tmp/${txt}-1 /tmp/${txt}-2"
  echo $cmd
  eval $cmd
else
  echo "do '$g1' and '$g2' exist, and are they gtfs .zip files?"
fi
