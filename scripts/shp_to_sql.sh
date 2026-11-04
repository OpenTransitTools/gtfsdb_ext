#
# create .sql files from .shp file using shp2pgsql
#
# directory structure:
#  -  ~/shp/                -- shp .sql files for the default ('current') schema
#  -  ~/shp/<agency>        -- shp .sql files for <agency> schema, ala ~/shp/trimet/service_district.sql
#  -  service_district.shp  -- for any files named 'service_district', create an ADA boundary ala trimet.ada
#
SHDIR=`dirname $0`

SHP_DIR=${1:-"$HOME/shp"}
DEF_SCHEMA=${2:-"current"}
SHP_2_PG=${3:-"$HOME/db/scripts/shp2pg.sh"}


function shp2pg() {
  shp_files="$1"
  shp_base_name=$(basename $SHP_DIR)

  for s in $shp_files
  do
    docker_shp_dir="/shp"
    schema=$DEF_SCHEMA
    out_dir=$SHP_DIR

    file_name=$(basename $s)                     # 'service_district.shp'
    file_base_name=${file_name%%.shp}            # 'service_district'
    parent_dir=$(basename "$(dirname "$s")")     # 'trimet' - e.g., dir name containing the .shp file

    if [ $parent_dir != $shp_base_name ]; then
      schema=$parent_dir
      docker_shp_dir="/shp/${parent_dir}"        # '/shp/trimet'
      out_dir=$SHP_DIR/$parent_dir               # '~/shp/trimet'
    fi
    table="${schema}.${file_base_name}"          # 'trimet.service_district'
    #echo "shp dir: $shp_base_name,  out dir: $out_dir,  file: $file_name,  schema: $schema,  table: $table"

    cmd="$SHP_2_PG ${docker_shp_dir}/${file_name} ${table} > $out_dir/${file_base_name}.sql"
    echo $cmd
    eval $cmd
  done
}


shp2pg "$SHP_DIR/*.shp"     # etl all .shp files that will go into common schema ('current')
shp2pg "$SHP_DIR/*/*.shp"   # etl the agency-specific .shp files, which will go in <agency> schema
