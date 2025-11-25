import csv
import requests
from . import utils


def to_csv(json, output):
    """
    create a stops.csv for Pelias

    id,name,lat,lon,source,layer,name_json,addendum_json_gtfs
    TRIMET:9992999,A Ave & Chandler (TriMet Stop ID 2),45.420609,-122.675671,transit,TRIMET_stops,"[""2"", ""9992999""]",
      "{""stop_code"":""2"",""stop_description"":""Stop in LO"",""url"":""https://agency.org/stop/2"",""location_type"":""1"",""direction"":""East"",""dir"":""E"",""position"":""Nearside""}"    
    """
    def to_addendum_json(stop, feed_id):
        si = '"stop_id":"{}",'.format(stop.stop_id) if stop.stop_id else ""
        sc = '"stop_code":"{}",'.format(stop.get_stop_code()) if stop.get_stop_code() else ""
        sd = '"stop_description":"{}",'.format(stop.stop.stop_desc) if stop.stop.stop_desc else ""
        lt = '"location_type":{},'.format(stop.stop.location_type or "0")
        f  = '"feed_id":"{}",'.format(feed_id)
        a  = '"agency_id":"{}",'.format(stop.agency_id) if stop.agency_id else ""
        u  = '"url":"{}",'.format(stop.stop.stop_url) if stop.stop.stop_url else ""
        d  = '"direction":"{}",'.format(stop.stop.direction) if stop.stop.direction else ""
        r  = '"dir":"{}",'.format(utils.direction_to_dir(stop.stop.direction))
        p  = '"position":"{}",'.format(stop.stop.position) if stop.stop.position else ""
        s  = '"shared":"{}",'.format(stop.stop.shared_stops) if stop.stop.shared_stops else ""
        m  = '"mode":"{}"'.format(stop.route_mode or "BUS")
        return '{{{}{}{}{}{}{}{}{}{}{}{}{}}}'.format(f, a, si, sc, sd, lt, u, d, r, p, s, m)

    layer = "pr"
    source = "transit"
    n = utils.make_pelias_csv_record(layer=layer, source=source, aliases=" ")

    writer = csv.DictWriter(output, fieldnames=n.keys())
    writer.writeheader()
    for i, r in enumerate(json):
        name = r.get('name')
        if name:
            alias = ""
            pr = ["pr", "p+r", "p&r", "park and", "park &", "parking"]
            if all(x not in name.lower() for x in pr):
                name = "{} PR".format(name)
                alias = utils.to_alias_json(name, r.get('name'))
            n['id'] = "pr-{}".format(i+1)
            n['name_json'] = alias
            utils.set_name_lat_lon(n, name, r.get('y'), r.get('x'))
            writer.writerow(n)



def query(url="https://ws.trimet.org/rtp/routers/default/park_and_ride"):
    ret_val = None
    response = requests.get(url)
    ret_val = response.json()
    return ret_val


def main():
    #import pdb; pdb.set_trace()
    json = query()
    file = "p"
    #file = "pr.csv"
    if file.lower() in ("p", "print"):
        import io
        output = io.StringIO()
        to_csv(json, output)
        print(output.getvalue())
    else:
        with open(file, 'w') as output:
            to_csv(json, output)

