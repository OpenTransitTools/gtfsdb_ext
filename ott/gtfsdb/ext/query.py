from gtfsdb.util import do_sql
from .utils import *

import logging
log = logging.getLogger(__name__)


def list_schemas(db, table="stops"):
    sql = f"SELECT schemaname FROM pg_catalog.pg_tables WHERE tablename = '{table}'"
    rez = do_sql(db, sql)
    ret_val = [' '.join(item) for item in rez]
    return ret_val


def clear_columns(db):
    for table in ["stops", "current_stops"]:
        for schema in list_schemas(db, table):
            sql = f"UPDATE {schema}.{table} SET shared_stops = NULL"
            #print(sql)
            do_sql(db, sql)



def to_stop_dict(rec, i=0, feed_id=None, def_agency=None, table="current_stops", distance=None):
    """
    stupid sql record mapping
    note: slightly fragile ... if gtfsdb model for stops changes (doesn't happen often), this might break
    """
    ret_val = None
    try:
        a = def_agency
        if table == "current_stops":
            a = rec[i+6]
        if a is None:
            a = def_agency

        ret_val = {
            'agency_id': a,
            'feed_id': feed_id,
            'stop_id': rec[i],
            'stop_code': rec[i + 1],
            'lat': rec[i + 2],
            'lon': rec[i + 3],
            'name': rec[i + 4],
            'distance': distance
        }
    except:
        ret_val = None
    return ret_val


def set_shared_stop(db, shared_stops_val, feed_id, stop_id, table="stops"):
    sql = f"UPDATE {feed_id}.{table} SET shared_stops = '{shared_stops_val}' WHERE stop_id = '{stop_id}'"
    return do_sql(db, sql)


def find_stop(db, feed_id, stop_id, table="stops"):
    sql = f"select * from {feed_id}.{table} where stop_id = '{stop_id}'"
    return do_sql(db, sql)


def stop_distance(db, feed_id_a, stop_id_a, feed_id_b, stop_id_b):
    """"
    find distance between 2 stops, selected by stop_id (and feed_id)
    :return: distance in meters
    :note: https://postgis.net/docs/ST_DistanceSphere.html
    """
    sql = f"select ST_DistanceSphere(a.geom, b.geom) from {feed_id_a}.stops a, {feed_id_b}.stops b where a.stop_id = '{stop_id_a}' and b.stop_id = '{stop_id_b}'"
    return do_sql(db, sql)


def nearest_stops(db, feed_id, stop_id, src_feed_id, table="stops", limit=10):
  sql = f"select ST_DistanceSphere(a.geom, b.geom) as meters_apart, a.* from {feed_id}.{table} a, {src_feed_id}.stops b where b.stop_id = '{stop_id}' order by 1 limit {limit}"
  return do_sql(db, sql)


def nearest(db, feed_id, stop_id, dist, src_feed_id, table="stops"):
    #import pdb; pdb.set_trace()
    sql = f"select * from {feed_id}.{table} where ST_DWithin(stop.geom, (select t.geom from {src_feed_id}.stops t where stop_id = '{stop_id}'), {dist})"
    return do_sql(db, sql)


def agencies(db, feed_id, limit=50, table="agency"):
    sql = f"select * from {feed_id}.{table} limit {limit}"
    return do_sql(db, sql)


nearest_hits = {}
def is_already_seen(fs):
    global nearest_hits
    ret_val = False
    if fs in nearest_hits:
        ret_val = True
    nearest_hits[fs] = fs
    return ret_val
        

def get_nearest_record(db, feed_id, stop_id, query_dist, dist_desc, src_feed_id, ignore_seen_filter=False):
    ret_val = None

    from_current_stops = False
    from_stops_table = False

    result = nearest(db, feed_id, stop_id, query_dist, src_feed_id, "current_stops")
    if result:
        from_current_stops = True
    else:
        result = nearest(db, feed_id, stop_id, query_dist, src_feed_id, "stops")
        if result:
            from_stops_table = True

    dist = 1111111.11111111

    if from_current_stops or from_stops_table:
        src = mk_feed_rec(src_feed_id, stop_id, src_feed_id)  # todo: call current for actual agency id (PSC or AT)

        share = []
        for r in result:
            sid = None
            if from_stops_table:
                sid = r[0]
                rec = mk_feed_rec(feed_id, sid)
            elif from_current_stops:
                sid = r[7]
                rec = mk_feed_rec(feed_id, sid, r[0])

            dist = stop_distance(db, src_feed_id, stop_id, feed_id, sid)

            if rec and (ignore_seen_filter or not is_already_seen(rec)):
                share.append(rec)

        if share:
            ret_val = { 
                'src': src,
                'dist': dist,
                'query_dist': query_dist,
                'dist_desc': dist_desc,
                'share': share
            }

    return ret_val
