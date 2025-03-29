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
                        ret_val[NOT_FOUND].append({'feed_stop': mk_feed_stop(src_feed_id, stop_id), 'share': feed_id})
    return ret_val


def create_report():
    from . import report
    args, kwargs = get_args()
    db = Database(**kwargs)
    ss = shared_stops_parser(args.file, db)

    report.generate_report(ss)