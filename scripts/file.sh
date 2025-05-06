DIR=`dirname $0`
. $DIR/base.sh

sql_file=${1:-"NOPE"}

if [ -f $sql_file ]; then
  if [[ "$psql" == *"docker"* ]]; then
    r="$pg_restore -d ${ott_url} < $sql_file"
  else
    r="$psql ${ott_url} -f $sql_file"
  fi
  echo loading .sql file: $sql_file
  echo $r
  eval $r
elif [ $sql_file == "NOPE" ]; then
  echo "file.sh <sql commands .sql>"
else
  echo "$sql_file doesn't exist"
fi
