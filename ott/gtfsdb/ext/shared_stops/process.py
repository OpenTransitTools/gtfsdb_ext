from gtfsdb import Database
from gtfsdb.util import get_csv
from gtfsdb.scripts import get_args

from .. import query
from ..utils import *

#import os
#import inspect
#this_module_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

def update_db(stops_csv_file, db, src_feed_id="TRIMET"):
    stop_dict = get_csv(stops_csv_file)
    for s in stop_dict:

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


def build_shared_stops_data(stops_csv_file, db, src_feed_id="TRIMET"):
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


def db_rec_to_shared_stop(rec, required=1):
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
        d = n[0]
        if i >= required and d > p + 1.0:
            break
        p = d
        if i == 0:
            distance = d

        m = query.to_stop_dict(n, 1, feed_id=feed, def_agency=def_ag, distance=d)
        stops.append(m)

    ret_val = {
        'desc': "{} -> {}({}) ".format(id, desc, aid),
        'distance': distance,
        'stops': stops
    }
    return ret_val


def shared_stops_parser(csvfile, db):
    unsuppored = {}
    no_stop = {}

    ret_val = {
        'unsuppored': unsuppored,
        'no_stop': no_stop,
        'shared': []
    }

    # step 1: grab the csv file, and then query the db and append stop and nearest stop data
    stop_recs = build_shared_stops_data(csvfile, db)

    # step 2: count the number of times we have FEED:STOP (some stop ids serve multiple agencies)
    counts = {}
    for s in stop_recs:
        fs = mk_feed_stop(s['FEED_ID'], s['STOP_ID'])
        if counts.get(fs) is None:
            counts[fs] = 1
        else:
            counts[fs] = counts[fs] + 1
    #import pdb; pdb.set_trace()

    # step 3: run thru filter out / fill in stop data, etc...
    for s in stop_recs:
        fs = mk_feed_stop(s['FEED_ID'], s['STOP_ID'])
        required = counts.get(fs)
        #import pdb; pdb.set_trace()

        src = s.get('src_stop')
        agy = s.get('agencies')
        if agy:
            if src:
                z = db_rec_to_shared_stop(s, required)
                x = query.to_stop_dict(src[0], feed_id="TRIMET", distance=z.get('distance'))
                z['stops'].insert(0, x)
                ret_val['shared'].append(z)
            else:
                no_stop[s.get('TRIMET_ID')] = s
        else:
            unsuppored[s.get('AGENCY_DESC')] = s.get('AGENCY_DESC')

    return ret_val


def update_shared_stops():
    args, kwargs = get_args()
    db = Database(**kwargs)
    #ss = shared_stops_parser(args.file, db)
    ss = update_db(args.file, db)


def create_report():
    from . import report
    args, kwargs = get_args()
    db = Database(**kwargs)
    ss = shared_stops_parser(args.file, db)
    report.generate_report(ss)

