
from gtfsdb import Database
from gtfsdb.util import get_csv
from gtfsdb.scripts import get_args

from . import report
from .. import query
from ..utils import *


def update_db(shared_stops, db, src_feed_id):
    for s in shared_stops:

        # step 1: get stop_id we're looking for in given feed_id
        stop_id = s['STOP_ID']
        feed_id = s['FEED_ID']

        stop = query.find_stop(db, src_feed_id, stop_id)
        if stop:
            print(stop)
            query.set_shared_stop(db, "X {} X".format(stop_id), src_feed_id, stop_id)
            query.set_shared_stop(db, "X {} X".format(stop_id), src_feed_id, stop_id, "CURRENT_STOPS")
        else:
            print("{}.{} not found in the feed.".format(src_feed_id, stop_id))


def build_shared_stops_data(stops_csv_file, db, src_feed_id):
    """
    build a fairly complex data structure based on:
     a) shared stops .csv (query from TRANS)
     b) stop info from gtfsdb (for trimet stop)
     b) nearest stops (gtfsdb) from other agencies
     c) current stops data (agency id)

    reads shared_stops.csv, then queries the database to build upon that structure 
    """
    stop_dict = get_csv(stops_csv_file)

    for s in stop_dict:
        s['agencies'] = None
        s['src_stop'] = None
        s['nearest'] = []

        # step 1: get stop_id we're looking for in given feed_id
        feed_id = s['FEED_ID']
        stop_id = s['STOP_ID']

        # step 2: make sure we have an agency for this feed (else might be a non-supported feed)
        agencies = query.agencies(db, feed_id)
        if not agencies:
            continue
        s['agencies'] = agencies

        # step 3: get the target stop record (continue if we don't have a source stop ... ala not in feed)
        stop = query.find_stop(db, src_feed_id, stop_id, "CURRENT_STOPS")
        if not stop:
            stop = query.find_stop(db, src_feed_id, stop_id)       
        if not stop:
            continue
        s['src_stop'] = stop

        # step 4: nearest shared stops
        s['nearest'] = query.nearest_stops(db, feed_id, stop_id, src_feed_id, table="STOPS", limit=5)

    return stop_dict


def db_rec_to_shared_stop(rec, skip=0):
    # step 1: parse the elements from shared_stops.csv    
    id=rec.get('STOP_ID')
    desc=rec.get('AGENCY_DESC')
    aid=rec.get('AGENCY')
    feed=rec.get('FEED_ID')

    # step 2: find all the agencies for a given feed
    age=rec.get('agencies')
    def_ag = "?"
    if age:
        if len(age) == 1:
            def_ag = age[0][1]
        else:
            def_ag = age[0][1] + "?"

    # step 3: nearest stops
    stops = []
    distance = None
    p = 444444.4
    near = rec.get('nearest')
    for i, n in enumerate(near):
        if i < skip:
            #import pdb; pdb.set_trace()
            continue
        d = n[0]
        if d > p + 1.0:
            break
        p = d
        distance = d

        m = query.to_stop_dict(n, 1, feed_id=feed, def_agency=def_ag, distance=d)
        stops.append(m)

    ret_val = {
        'desc': "{} -> {}({}) ".format(id, desc, aid),
        'distance': distance,
        'stops': stops
    }
    return ret_val


def make_skips(stop_recs, start=0):
    """ utility to build dict that counts the feed/stop pairs """
    skips = {}
    for s in stop_recs:
        fs = mk_feed_stop(s['FEED_ID'], s['STOP_ID'])
        if skips.get(fs) is None:
            skips[fs] = start
        else:
            skips[fs] = skips[fs] + 1
    return skips



def shared_stops_parser(csvfile, db, src_feed_id):
    unsuppored = {}
    no_stop = {}

    ret_val = {
        'unsuppored': unsuppored,
        'no_stop': no_stop,
        'shared': []
    }

    # step 1: grab the csv file, and then query the db and append stop and nearest stop data
    stop_recs = build_shared_stops_data(csvfile, db, src_feed_id)

    # step 2: make skips (used in step 3) to determine if we have repeat stops, and need a the next nearest stop
    skips = make_skips(stop_recs)

    # step 2: run thru stop data to build up stops list, etc...
    for s in stop_recs:
        fs = mk_feed_stop(s['FEED_ID'], s['STOP_ID'])
        src = s.get('src_stop')
        agy = s.get('agencies')
        if agy:
            if src:
                #import pdb; pdb.set_trace()
                z = db_rec_to_shared_stop(s, skips[fs])
                x = query.to_stop_dict(src[0], feed_id="TRIMET", distance=z.get('distance'))
                z['stops'].insert(0, x)
                ret_val['shared'].append(z)
                skips[fs] = skips[fs] - 1  # decriment skips, so that we pick up nearer stops on next hits
            else:
                no_stop[s.get('STOP_ID')] = s['FEED_ID']
        else:
            unsuppored[s.get('AGENCY_DESC')] = s.get('AGENCY_DESC')

    # step 3a TODO: filter duplicates part A - count the number duplicate FEED:STOP
    counts = {}
    for s in stop_recs:
        fs = mk_feed_stop(s['FEED_ID'], s['STOP_ID'])
        if counts.get(fs) is None:
            counts[fs] = 1
        else:
            counts[fs] = counts[fs] + 1
    #import pdb; pdb.set_trace()

    return ret_val


def cmd_line_get_shared_stops():
    args, kwargs = get_args()
    db = Database(**kwargs)
    ss = shared_stops_parser(args.file, db, args.schema)
    return args, db, ss


def update_shared_stops():
    args, db, ss = cmd_line_get_shared_stops()
    update_db(ss, db, args.schema)
