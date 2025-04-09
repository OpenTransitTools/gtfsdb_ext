if [ -d ~/gtfs/cache ]; then
  GTFS_DIR=~/gtfs/cache
elif [ -d ~/gtfsdb/cache ]; then
  GTFS_DIR=~/gtfsdb/cache
elif [ -d ~/gtfs ]; then
  GTFS_DIR=~/gtfs
else
  GTFS_DIR=~/gtfsdb
fi

function feed_name_from_zip() {
  # get lowercase feed name from gtfs .zip file name
  # ala '../FEED_NAME.gtfs.zip' -> 'feed_name' 
  name=${1#$GTFS_DIR/}
  name=${name%.gtfs.zip}
  name=$(echo "$name" | awk '{print tolower($1)}')
  echo $name
}

mac_psql=/Applications/Postgres.app/Contents/Versions/9.4/bin/psql
unix_psql=`which psql`
pg_restore=pg_restore

if [ -f "$mac_psql" ]
then
  psql=$mac_psql
elif [ -f "$unix_psql" ]
then
  psql=$unix_psql
fi

db_url=$1
def_db=${2:-postgres}

# IMPORTANT: there are are python configs for user, pass and db in loader/config/app.ini, which also need to change
user=ott
pass=ott
db=ott
osm_db=osm
otp_url=postgresql://$user:$pass@127.0.0.1:5432/$db

# use URL if we get content on the cmd line (default to docker url when no ://)
if  [[ "$db_url" != "" ]] && [[ "$db_url" != *"://"* ]]; then
    db_url=postgres://docker:docker@localhost:5432/
fi
