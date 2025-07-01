import csv
from gtfsdb import Database
from gtfsdb.scripts import get_args
from gtfsdb import *
from gtfsdb import util


def to_csv(stops, feed_id, output):
    # id,name,lat,lon,source,layer,addendum_json_gtfs
    # TRIMET:22,A Ave & Chandler (TriMet Stop ID 2),45.420609,-122.675671,transit,TRIMET_stops,
    #  "{""stop_code"":""2"",""stop_description"":""Stop in LO"",""url"":""https://agency.org/stop/2"",""location_type"":""1"",""direction"":""East"",""position"":""Nearside""}"    

    def to_addendum_json(stop, feed_id):
        #return "{""stop_code"":""{}""
        #return """stop_code\"\":\"\"{}\"\"".format(stop.get_stop_code())
        sc = '"stop_code":"{}",'.format(stop.get_stop_code()) if stop.get_stop_code() else ""
        sd = '"stop_description":"{}",'.format(stop.stop.stop_desc) if stop.stop.stop_desc else ""
        lt = '"location_type":{},'.format(stop.stop.location_type or "0")
        f  = '"feed_id":"{}",'.format(feed_id)
        a  = '"agency_id":"{}",'.format(stop.agency_id) if stop.agency_id else ""
        u  = '"url":"{}",'.format(stop.stop.stop_url) if stop.stop.stop_url else ""
        d  = '"direction":"{}",'.format(stop.stop.direction) if stop.stop.direction else ""
        p  = '"position":"{}",'.format(stop.stop.position) if stop.stop.position else ""
        s  = '"shared":"{}",'.format(stop.stop.shared_stops) if stop.stop.shared_stops else ""
        m  = '"mode":"{}"'.format(stop.route_mode or "BUS")
        return '{{{}{}{}{}{}{}{}{}{}{}}}'.format(f, a, sc, sd, lt, u, d, p, s, m)

    layer = feed_id + "_stops"
    source = "transit"
    n = {"id":"", "name":"", "lat":0.0, "lon":0.0, "source": source, "layer": layer, "addendum_json_gtfs": ""}

    writer = csv.DictWriter(output, fieldnames=n.keys())
    writer.writeheader()
    for s in stops:
        n['id'] = "{}:{}".format(feed_id, s.stop_id)
        n['name'] = "{} ({} Stop ID {})".format(s.stop_name, s.stop.agency_name, s.get_stop_code())
        n['lat'] = s.stop_lat
        n['lon'] = s.stop_lon
        n['addendum_json_gtfs'] = to_addendum_json(s, feed_id)
        writer.writerow(n)


def query(feed, output, url="postgresql://ott@localhost:5432/ott"):
    db = Database(url=url, schema=feed.lower())
    stops = CurrentStops.query_stops(db.session())
    to_csv(stops, feed, output)


def main():
    #import pdb; pdb.set_trace()
    args, kwargs = get_args(def_db="postgresql://ott@localhost:5432/ott", def_schema='SMART')
    if len(args.file) < 4:
        import io
        output = io.StringIO()
        query(args.feed_id, output, args.database_url)
        print(output.getvalue())
    else:
        with open(args.file, 'w') as output:
            query(args.feed_id, output, args.database_url)
