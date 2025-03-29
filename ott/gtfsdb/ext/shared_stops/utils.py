NOT_FOUND = "not found"
INCHES_AWAY = "inches away"
FEET_AWAY = "feet away"
YARDS_AWAY = "yards away"
BLOCKS_AWAY = "blocks away"

IGNORE_AGENCIES = ['CANBY', 'CCRIDER', 'CAT', 'YAMHILL']


def mk_feed_stop(feed_id, stop_id):
    return "{}:{}".format(feed_id, stop_id)


def mk_feed_rec(feed_id, stop_id, agency_id="?"):
    return "{}:{}:{}".format(agency_id, feed_id, stop_id)
