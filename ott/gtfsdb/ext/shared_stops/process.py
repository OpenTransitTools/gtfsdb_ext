from gtfsdb import Database
from gtfsdb.util import get_csv
from gtfsdb.scripts import get_args

from . import query
from .utils import *

#import os
#import inspect
#this_module_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


def shared_stops_parser(stops_csv_file, db, src_feed_id="TRIMET"):
    """
    simple shared stops read
    reads shared_stops.csv, and match up with agency id from feed_agency.csv
    format:  feed_id:agency_id:stop_id,...
    example: "TRIMET:TRIMET:7646,CTRAN:C-TRAN:5555,RIDECONNECTION:133:876575"
    """
    ret_val = {
        'src': [],
        NOT_FOUND: [],
        INCHES_AWAY: [],
        FEET_AWAY: [],
        YARDS_AWAY: [],
        BLOCKS_AWAY: []
    }

    stop_dict = get_csv(stops_csv_file)
    for s in stop_dict:

        # step 1: get stop_id we're looking for in given feed_id
        stop_id = s['TRIMET_ID']
        feed_id = s['FEED_ID']

        # step 2: skip unsupported agencies
        if feed_id in IGNORE_AGENCIES:
            continue

        # step 3: save off this shared stop (reporting)
        ret_val['src'].append(s)

        # step 4: progressively find nearest stops based on distance
        result = query.get_nearest_record(db, feed_id, stop_id, 0.00013, INCHES_AWAY, src_feed_id)
        if result:
            ret_val[INCHES_AWAY].append(result)
        else:
            result = query.get_nearest_record(db, feed_id, stop_id, 0.00033, FEET_AWAY, src_feed_id)
            if result:
                ret_val[FEET_AWAY].append(result)
            else:
                result = query.get_nearest_record(db, feed_id, stop_id, 0.00066, YARDS_AWAY, src_feed_id)
                if result:
                    ret_val[YARDS_AWAY].append(result)
                else:
                    result = query.get_nearest_record(db, feed_id, stop_id, 0.0055, BLOCKS_AWAY, src_feed_id)
                    if result:
                        ret_val[BLOCKS_AWAY].append(result)
                    else:
                        ret_val[NOT_FOUND].append({'feed_stop': mk_feed_stop(src_feed_id, stop_id), 'share': feed_id, 's': s})
    return ret_val


def update_db(stops_csv_file, db, src_feed_id="TRIMET"):
    stop_dict = get_csv(stops_csv_file)
    for s in stop_dict:

        # step 1: get stop_id we're looking for in given feed_id
        stop_id = s['TRIMET_ID']
        feed_id = s['FEED_ID']

        # step 2: skip unsupported agencies
        if feed_id in IGNORE_AGENCIES:
            continue

        stop = query.find_stop(db, src_feed_id, stop_id, "CURRENT_STOPS")
        if not stop:
            stop = query.find_stop(db, src_feed_id, stop_id)
        if stop:
            print(stop)
            query.set_shared_stop(db, "X {} X".format(stop_id), src_feed_id, stop_id)
            query.set_shared_stop(db, "X {} X".format(stop_id), src_feed_id, stop_id, "CURRENT_STOPS")
        else:
            print("{}.{} not found in the feed.".format(src_feed_id, stop_id))


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
        stop_id = s['TRIMET_ID']  # todo change this to STOP_ID
        feed_id = s['FEED_ID']

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


def create_report():
    from . import report
    args, kwargs = get_args()
    db = Database(**kwargs)
    ss = build_shared_stops_data(args.file, db)
    print(ss)
