spool shared_stops.csv;
select /*csv*/ distinct rs.location_id as stop_ID, 
r.transit_agency_id as agency,
rd.route_usage_description as agency_desc,
CASE 
WHEN r.transit_agency_id = 1 THEN 'CTRAN'
WHEN r.transit_agency_id = 2 THEN 'SMART'
WHEN r.transit_agency_id = 3 THEN 'SAM'
WHEN r.transit_agency_id = 4 THEN 'CCRIDER'
WHEN r.transit_agency_id = 5 THEN 'CCRIDER'
WHEN r.transit_agency_id = 6 THEN 'YAMHILL'
WHEN r.transit_agency_id = 7 THEN 'WAPARK'
WHEN r.transit_agency_id = 11 THEN 'CAT'
WHEN r.transit_agency_id = 12 THEN 'CANBY'
WHEN r.transit_agency_id = 13 THEN 'CLACKAMAS'
WHEN r.transit_agency_id = 16 THEN 'CLACKAMAS'
WHEN r.transit_agency_id = 14 THEN 'RIDECONNECTION'
WHEN r.transit_agency_id = 15 THEN 'MULT'
ELSE 'UNKNOWN'
END as FEED_ID
from trans.route_stop_def rs, trans.route r, trans.route_usage_description rd
where rs.route_stop_begin_date < sysdate
and rs.route_stop_end_date > sysdate
and rs.route_number = r.route_number
and r.transit_agency_id = rd.transit_agency_id
and r.transit_agency_id > 0 and r.transit_agency_id != 8
order by 1,2;
spool off;
