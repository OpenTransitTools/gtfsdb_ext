"""
NOTE - are these routines even used?  Moved here from query.py
"""
#from .. import query


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

    result = query.nearest(db, feed_id, stop_id, query_dist, src_feed_id, "current_stops")
    if result:
        from_current_stops = True
    else:
        result = query.nearest(db, feed_id, stop_id, query_dist, src_feed_id, "stops")
        if result:
            from_stops_table = True

    dist = 1111111.11111111

    if from_current_stops or from_stops_table:
        src = query.mk_feed_rec(src_feed_id, stop_id, src_feed_id)  # todo: call current for actual agency id (PSC or AT)

        share = []
        for r in result:
            sid = None
            if from_stops_table:
                sid = r[0]
                rec = query.mk_feed_rec(feed_id, sid)
            elif from_current_stops:
                sid = r[7]
                rec = query.mk_feed_rec(feed_id, sid, r[0])

            dist = query.stop_distance(db, src_feed_id, stop_id, feed_id, sid)

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
