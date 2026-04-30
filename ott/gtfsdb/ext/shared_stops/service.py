import re
from ott.utils import file_utils
from ott.utils import web_utils
from .. import query

import logging
log = logging.getLogger(__name__)


def put_db(db, feed_id, stop_id, shared_string, table, test=False):
    try:
        add_ss = True

        # step 1: check that the stop exists, and report any that aren't there
        if test:
            z = query.find_stop(db, feed_id, stop_id, table)
            if z is None or len(z) < 1:
                print(f"note: {feed_id}.{table} lacks stop '{stop_id}', so can't add shared '{shared_string}'")

        # step 2: make sure the TRIMET stop is there (if not, we don't want to filter the agency stop from the stops layer)
        if feed_id != "TRIMET":
            match = re.search(r"TRIMET:(.*?),", shared_string)
            tm_stop = match.group(1)
            z = query.find_stop(db, "TRIMET", tm_stop, table)
            if z is None or len(z) < 1:
                print(f"note: {tm_stop} not in TRIMET.{table}, won't add '{shared_string}' to {feed_id}.{table} for {stop_id}")
                add_ss = False

        # step 3: update the db with this shared stop string
        if add_ss:
            query.set_shared_stop(db, shared_string, feed_id, stop_id, table)
    except Exception as e:
        log.warning(e)


def put(db, ss):
    try:
        #import pdb; pdb.set_trace()
        """ CTRAN:4 -> CTRAN,4 """
        feed_id, stop_id = ss['feed_stop_id'].split(":", 1)
        shared_string = ss['shared_string']
        put_db(db, feed_id, stop_id, shared_string, "stops")
        put_db(db, feed_id, stop_id, shared_string, "current_stops", True)
    except Exception as e:
        log.warning(e)


def update_parsed_stops(sstops, db):
    """
    put data from service into stops and current_stops tables
    """
    for ss in sstops:
        put(db, ss)


def call_service(ss_url):
    """
    service should return array in the form of: [
      {'stop': 'TRIMET:7612', 'shared_string': 'TRIMET:7612,CTRAN:5005', 'distance': '0.03212339'},
      {'stop': 'CTRAN:5005', 'shared_string': 'TRIMET:7612,CTRAN:5005', 'distance': '0.03212339'}
    ]
    """
    ssv = "ss.csv"
    web_utils.wget(ss_url, ssv)
    sstops = file_utils.read_csv(ssv)
    return sstops
