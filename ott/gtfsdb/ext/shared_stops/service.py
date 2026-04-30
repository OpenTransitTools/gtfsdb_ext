from ott.utils import file_utils
from ott.utils import web_utils
from .. import query

import logging
log = logging.getLogger(__name__)


def put_db(db, feed_id, stop_id, shared_string, table):
    try:
        z = query.find_stop(db, feed_id, stop_id, table)
        if z is None or len(z) < 1:
            print(f"note: {feed_id}.{stop_id} in table {table} doesn't seem to exist to add {shared_string}")

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
        put_db(db, feed_id, stop_id, shared_string, "current_stops")
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
