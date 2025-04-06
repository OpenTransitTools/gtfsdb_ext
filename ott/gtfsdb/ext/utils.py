NOT_FOUND = "not found"
INCHES_AWAY = "inches away"
FEET_AWAY = "feet away"
YARDS_AWAY = "yards away"
BLOCKS_AWAY = "blocks away"

IGNORE_AGENCIES = ['CANBY', 'CCRIDER', 'CAT', 'YAMHILL']


def mk_feed_stop(feed_id, stop_id=""):
    if isinstance(feed_id, dict):
        so = feed_id
        feed_id = so.get("FEED_ID", so.get("feed_id", feed_id))
        stop_id = so.get("STOP_ID", so.get("stop_id", stop_id))
        
    return "{}:{}".format(feed_id, stop_id)


def mk_feed_rec(feed_id, stop_id, agency_id="?"):
    if isinstance(feed_id, dict):
        so = feed_id
        feed_id = so.get("FEED_ID", so.get("feed_id", feed_id))
        stop_id = so.get("STOP_ID", so.get("stop_id", stop_id))
        agency_id = so.get("AGENCY_ID", so.get("agency_id", agency_id))

    return "{}:{}:{}".format(agency_id, feed_id, stop_id)


def strip_agency_id(id):
    "C-TRAN:CTRAN:4 becomes CTRAN:4"
    ret_val = id
    parts = id.split(":", 1)
    if len(parts) > 1:
        ret_val = parts[1]
    return ret_val
