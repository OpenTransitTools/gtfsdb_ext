DIR=`dirname $0`
. $DIR/base.sh

sql_file=${1:-"NOPE"}

if [ -f $sql_file ]; then
  echo loading .sql file: $sql_file
  r="$psql ${otp_url} -f $sql_file"
  echo $r
  eval $r
elif [ $sql_file == "NOPE" ]; then
  echo "file.sh <sql commands .sql>"
else
  echo "$sql_file doesn't exist"
fi
