SCDIR=`dirname $0`
. $SCDIR/base.sh


# CREATE A <name>.schema file in the $GTFS_DIR, along with some other permission cmds
function make_schema() {
  schema=${1:-"current"}
  perms=${2:-"ALL"}
  users=${3:-"${user}"}

  echo "DROP SCHEMA IF EXISTS $schema CASCADE;" > $GTFS_DIR/${schema}.schema
  echo "CREATE SCHEMA $schema;" >> $GTFS_DIR/${schema}.schema
  echo "GRANT USAGE ON SCHEMA $schema TO $users;" >> $GTFS_DIR/${schema}.schema
  p="ALTER DEFAULT PRIVILEGES IN SCHEMA $schema GRANT $perms"
  echo "$p ON TABLES TO $users;" >> $GTFS_DIR/${schema}.schema
  echo "$p ON SEQUENCES TO $users;" >> $GTFS_DIR/${schema}.schema
}


# LOAD all $GTFS_DIR/<name>.schema files into the db
function load_schemas() {
  for s in ${GTFS_DIR}/*schema
  do
    echo "load schema(s): $s"
    r="${SCDIR}/file.sh $s"
    echo $r
    eval $r
    echo
  done
}
