from gtfsdb import Database
from gtfsdb import *
from gtfsdb import util


def to_addendum_json(stop):
    #return "{""stop_code"":""{}"",""stop_description"":""{}"",""url"":""{}"",""location_type"":""{}"",""direction"":""{}"",""position"":""{}""}".format(stop)
    return "{""stop_code"":""{code}""}".format(stop)


def to_csv(stops, feed, output):
    # id,name,lat,lon,source,layer,addendum_json_gtfs
    # TRIMET:22,A Ave & Chandler (TriMet Stop ID 2),45.420609,-122.675671,transit,TRIMET_stops,
    #  "{""stop_code"":""2"",""stop_description"":""Stop in LO"",""url"":""https://agency.org/stop/2"",""location_type"":""1"",""direction"":""East"",""position"":""Nearside""}"    
    import csv

    layer = feed + "_stops"
    source = "transit"
    n = {"id":"", "name":"", "lat":0.0, "lon":0.0, "source": source, "layer": layer, "addendum_json_gtfs": ""}


    writer = csv.DictWriter(output, fieldnames=n.keys())
    writer.writeheader()
    for s in stops:
        n['id'] = "{}:{}".format(feed, s.stop_id)
        n['name'] = "{} ({} Stop ID {})".format(s.stop_name, s.stop.agency_name, s.get_stop_code())
        n['lat'] = s.stop_lat
        n['lon'] = s.stop_lon
        #n['addendum_json_gtfs'] = to_addendum_json(s)
        writer.writerow(n)


def query():
    url="postgresql://fpurcell@localhost:5432/ott"
    feed='SMART'
    db = Database(url=url, schema=feed.lower())
    stops = CurrentStops.query_stops(db.session())
    #print(stops)
    
    # TODO file output
    import io; output = io.StringIO()
 
    to_csv(stops, feed, output)
    
    print(output.getvalue())
