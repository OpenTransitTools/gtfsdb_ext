agency=${1:-"trimet"}
ada_name=${2:-"ada"}
ada_file=${3:-"$HOME/shp/ada.sql"}

#
# buffer current route lines by 3,960 feet (3/4 mile), clipping the ada by the service district
# requires tables: <agency>.current_routes and <agency>.service_district
#
ADA_SQL=`cat <<EOF
DROP TABLE IF EXISTS ada_pattern_buffer;
CREATE TEMP TABLE ada_pattern_buffer AS
SELECT
    route_id,
    ST_Transform(
        -- buffer route lines by 3,960 feet (3/4 mile)
        ST_Buffer(
            ST_Transform(ST_SetSRID(geom, 4326), 2913), 
            3960
        ), 
        4326
    )::geometry(Polygon, 4326) AS geom
FROM ${agency}.current_routes
WHERE geom IS NOT NULL;
ALTER TABLE ada_pattern_buffer ADD PRIMARY KEY (route_id);

DROP TABLE IF EXISTS ${agency}.${ada_name};
CREATE TABLE ${agency}.${ada_name} AS
SELECT
  -- ST_Multi forces simple polygons (e.g. Polygon) into MultiPolygons
  ST_Multi(ST_Intersection(ST_MakePolygon(ST_ExteriorRing(ST_Union(pb.geom))), sd.geom))::geometry(MultiPolygon, 4326) AS geom
FROM 
  ada_pattern_buffer pb
-- an INNER JOIN 
INNER JOIN 
  -- clip ada boundary against the service district geometry
  ${agency}.service_district sd 
  ON ST_Intersects(pb.geom, sd.geom)
GROUP BY 
  sd.geom;
 
ALTER TABLE ${agency}.${ada_name} ADD COLUMN id SERIAL;
ALTER TABLE ${agency}.${ada_name} ADD PRIMARY KEY (id);
CREATE INDEX idx_${agency}_ada_geom ON ${agency}.${ada_name} USING GIST(geom);
EOF
`

echo "cat $ada_file"
echo "$ADA_SQL" > ${ada_file}
