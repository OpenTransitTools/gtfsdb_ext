if [ -d ~/gtfs/cache ]; then
  GTFS_DIR=~/gtfs/cache
elif [ -d ~/gtfsdb/cache ]; then
  GTFS_DIR=~/gtfsdb/cache
elif [ -d ~/gtfs ]; then
  GTFS_DIR=~/gtfs
else
  GTFS_DIR=~/gtfsdb
fi

mac_psql=/Applications/Postgres.app/Contents/Versions/9.4/bin/psql
unix_psql=`which psql 2> /dev/null`

user=${PG_USER:-ott}
pass=${PG_PASS:-ott}
db=${PG_DB:-ott}
def_user=${PG_DEF:-postgres}
dckr_url=${PG_URL:-postgresql://docker:docker@localhost:5432}
ott_url=${OTT_URL:-postgresql://$user:$pass@127.0.0.1:5432/$db}

if [ -f "$mac_psql" ]; then
  psql=$mac_psql
  pg_restore="pg_restore"
elif [ -f "$unix_psql" ]; then
  psql=$unix_psql
  pg_restore="pg_restore"
else
  docker_exe="docker exec -i -u $def_user"
  psql_term=${psql:-"$docker_exe -it db psql"}
  psql_ott=${psql:-"$docker_exe -e PGUSER=$user -e PGPASSWORD=$pass db psql"}
  psql=${psql:-"$docker_exe db psql"}
  pg_isready=${pg_isready:-"$docker_exe db pg_isready"}
  pg_restore=${pg_restore:-"$docker_exe db psql"}
  pg_dump=${pg_dump:-"$docker_exe db pg_dump"}
  pg_shp=${pg_shp:-"$docker_exe db shp2pgsql"}
fi


function feed_name_from_zip() {
  # get lowercase feed name from gtfs .zip file name
  # ala '../FEED_NAME.gtfs.zip' -> 'feed_name' 
  name=${1#$GTFS_DIR/}
  name=${name%.gtfs.zip}
  name=${name%.sql*}
  name=$(echo "$name" | awk '{print tolower($1)}')
  echo $name
}

