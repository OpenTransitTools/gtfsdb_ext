import csv
from gtfsdb import Database
from gtfsdb.scripts import get_args
from gtfsdb import *
from . import utils


def to_csv(stops, feed_id, output):
    """
    create a stops.csv for Pelias

    id,name,lat,lon,source,layer,addendum_json_gtfs,name_json
    TRIMET:9992999,A Ave & Chandler (TriMet Stop ID 2),45.420609,-122.675671,transit,TRIMET_stops
      "{""stop_code"":""2"",""stop_description"":""Stop in LO"",""url"":""https://agency.org/stop/2"",""location_type"":""1"",""direction"":""East"",""dir"":""E"",""position"":""Nearside""}",
      "[""2"", ""9992999""]",
    """
    #import pdb; pdb.set_trace()
    def to_popularity(stop, feed_id):
        inc = 1
        if feed_id in ("TRIMET"):
            inc = 5000
        elif feed_id in ("CTRAN", "SMART"):
            inc = 2000
        return int(10000+inc)

    def to_addendum_json(stop, feed_id):
        si = '"stop_id":"{}",'.format(stop.stop_id) if stop.stop_id else ""
        sc = '"stop_code":"{}",'.format(stop.get_stop_code()) if stop.get_stop_code() else ""
        sd = '"stop_description":"{}",'.format(stop.stop.stop_desc) if stop.stop.stop_desc else ""
        lt = '"location_type":{},'.format(stop.stop.location_type or "0")
        f  = '"feed_id":"{}",'.format(feed_id)
        a  = '"agency_id":"{}",'.format(stop.agency_id) if stop.agency_id else ""
        u  = '"url":"{}",'.format(stop.stop.stop_url) if stop.stop.stop_url else ""
        d  = '"direction":"{}",'.format(stop.stop.direction) if stop.stop.direction else ""
        r  = '"dir":"{}",'.format(utils.direction_to_dir(stop.stop.direction)) if stop.stop.direction else ""
        p  = '"position":"{}",'.format(stop.stop.position) if stop.stop.position else ""
        s  = '"shared":"{}",'.format(stop.stop.shared_stops) if stop.stop.shared_stops else ""
        m  = '"mode":"{}"'.format(stop.route_mode or "BUS")
        return '{{{}{}{}{}{}{}{}{}{}{}{}{}}}'.format(f, a, si, sc, sd, lt, u, d, r, p, s, m)

    def make_stop_name(stop, feed_id):
        # stop name with agency and stop_code info appended
        agency = stop.stop.agency_name or feed_id.capitalize()
        code = stop.get_stop_code()
        if code:
            ret_val = f"{stop.stop_name} ({agency} Stop ID {code})"
        else:
            ret_val = f"{stop.stop_name} ({agency} Stop)"
        return ret_val

    # output the pelias .csv data
    writer = None
    for s in stops:
        feed_stop_id = f"{feed_id}:{s.stop_id}"
        rec = utils.make_pelias_csv_record(
            id=feed_stop_id,
            layer=feed_id + ":stops", source="transit",
            name=make_stop_name(s, feed_id),
            lat=s.stop_lat, lon=s.stop_lon,
            popularity=to_popularity(s, feed_id),
            aliases=utils.to_alias_json(s.stop_id, s.get_stop_code() or feed_stop_id),
            addendum=to_addendum_json(s, feed_id)
        )

        # create the output csv writer on first pass
        if writer is None:
            writer = csv.DictWriter(output, fieldnames=rec.keys())
            writer.writeheader()

        writer.writerow(rec)


def query(feed, output, url="postgresql://ott:ott@localhost:5432/ott"):
    db = Database(url=url, schema=feed.lower())
    stops = CurrentStops.query_stops(db.session())
    to_csv(stops, feed, output)


def main():
    #import pdb; pdb.set_trace()
    args, kwargs = get_args(prog_name='pelias-stops', def_db="postgresql://ott:ott@localhost:5432/ott", def_schema='SMART')
    if args.file.lower() in ("p", "print"):
        import io
        output = io.StringIO()
        query(args.feed_id, output, args.database_url)
        print(output.getvalue())
    else:
        with open(args.file, 'w') as output:
            query(args.feed_id, output, args.database_url)
