from gtfsdb.util import do_sql
from .utils import *

import logging
log = logging.getLogger(__name__)


def to_stop_dict(rec, i=0, feed_id=None, def_agency=None, table="CURRENT_STOPS"):
    """
    stupid sql record mapping
    note: slightly fragile ... if gtfsdb model for stops changes (doesn't happen often), this might break
    """
    ret_val = None
    try:
        a = def_agency
        if table == "CURRENT_STOPS":
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
        }
    except:
        ret_val = None
    return ret_val


def set_shared_stop(db, shared_stops_val, feed_id, stop_id, table="STOPS"):
    sql = "UPDATE {}.{} SET shared_stops = '{}' WHERE stop_id = '{}'".format(feed_id, table, shared_stops_val, stop_id)
    return do_sql(db, sql)


def find_stop(db, feed_id, stop_id, table="STOPS"):
    sql = "select * from {}.{} where stop_id = '{}'".format(feed_id, table, stop_id)
    return do_sql(db, sql)


def stop_distance(db, feed_id_a, stop_id_a, feed_id_b, stop_id_b):
    """"
    find distance between 2 stops, selected by stop_id (and feed_id)
    :return: distance in meters
    :note: https://postgis.net/docs/ST_DistanceSphere.html
    """
    sql = "select ST_DistanceSphere(a.geom, b.geom) from {}.stops a, {}.stops b where a.stop_id = '{}' and b.stop_id = '{}'".format(feed_id_a, feed_id_b, stop_id_a, stop_id_b)
    return do_sql(db, sql)


def nearest_stops(db, feed_id, stop_id, src_feed_id, table="STOPS", limit=10):
  sql = "select ST_DistanceSphere(a.geom, b.geom) as meters_apart, a.* from {}.{} a, {}.stops b where b.stop_id = '{}' order by 1 limit {}".format(feed_id, table, src_feed_id, stop_id, limit)
  #print(sql)
  return do_sql(db, sql)


def nearest(db, feed_id, stop_id, dist, src_feed_id, table="STOPS"):
    sql = "select * from {}.{} stop where ST_DWithin(stop.geom, (select t.geom from {}.stops t where stop_id = '{}'), {})".format(feed_id, table, src_feed_id, stop_id, dist)
    #print(sql)
    return do_sql(db, sql)


def agencies(db, feed_id, limit=50, table="AGENCY"):
    sql = "select * from {}.{} limit {}".format(feed_id, table, limit)
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

    result = nearest(db, feed_id, stop_id, query_dist, src_feed_id, "CURRENT_STOPS")
    if result:
        from_current_stops = True
    else:
        result = nearest(db, feed_id, stop_id, query_dist, src_feed_id, "STOPS")
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
