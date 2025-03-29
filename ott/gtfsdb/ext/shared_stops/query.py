from gtfsdb.util import do_sql
from .utils import *

import logging
log = logging.getLogger(__name__)


def set_shared_stop(db, shared_stops_val, feed_id, stop_id, table="STOPS"):
    sql = "UPDATE {}.{} SET shared_stops = '{}' WHERE stop_id = '{}'".format(feed_id, table, shared_stops_val, stop_id)
    return do_sql(db, sql)


def find_stop(db, feed_id, stop_id, table="STOPS"):
    sql = "select * from {}.{} where stop_id = '{}'".format(feed_id, table, stop_id)
    return do_sql(db, sql)


def nearest(db, feed_id, stop_id, dist, src_feed_id, table="STOPS"):
    sql = "select * from {}.{} stop where st_dwithin(stop.geom, (select t.geom from {}.stops t where stop_id = '{}'), {})".format(feed_id, table, src_feed_id, stop_id, dist)
    return do_sql(db, sql)


nearest_hits = {}
def is_already_seen(fs):
    global nearest_hits
    ret_val = False
    if fs in nearest_hits:
        ret_val = True
    nearest_hits[fs] = fs
    return ret_val
        

def get_nearest_record(db, feed_id, stop_id, dist, dist_desc, src_feed_id, ignore_seen_filter=False):
    ret_val = None

    from_current_stops = False
    from_stops_table = False

    result = nearest(db, feed_id, stop_id, dist, src_feed_id, "CURRENT_STOPS")
    if result:
        from_current_stops = True
    else:
        result = nearest(db, feed_id, stop_id, dist, src_feed_id, "STOPS")
        if result:
            from_stops_table = True

    if from_current_stops or from_stops_table:
        src = mk_feed_rec(src_feed_id, stop_id, src_feed_id)  # todo: call current for actual agency id (PSC or AT)

        share = []
        for r in result:
            if from_stops_table:
                rec = mk_feed_rec(feed_id, r[0])
            elif from_current_stops:
                rec = mk_feed_rec(feed_id, r[7], r[0])

            if rec and (ignore_seen_filter or not is_already_seen(rec)):
                share.append(rec)

        if share:
            ret_val = { 
                'src': src,
                'dist': dist,
                'dist_desc': dist_desc,
                'share': share
            }

    return ret_val
