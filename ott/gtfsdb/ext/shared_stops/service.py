from ott.utils import file_utils
from ott.utils import web_utils
from .. import query


def put_db(db, ss):
    try:
        """ CTRAN:4 -> CTRAN,4 """
        feed_id, stop_id = ss['stop'].split(":", 1)
        shared_string = ss['shared_string']

        #import pdb; pdb.set_trace()
        z = query.find_stop(db, feed_id, stop_id, table="current_stops")
        if z is None or len(z) < 1:
            print(f"note: {feed_id}.{stop_id} doesn't seem to exist to add {shared_string}")
        
        query.set_shared_stop(db, shared_string, feed_id, stop_id, "stops")
        query.set_shared_stop(db, shared_string, feed_id, stop_id, "current_stops")
    except Exception as e:
        print(e)


def update_parsed_stops(sstops, db):
    """
    put data from service into stops and current_stops tables
    """
    for ss in sstops:
        put_db(db, ss)


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