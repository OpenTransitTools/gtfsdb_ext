import logging

NOT_FOUND = "not found"
INCHES_AWAY = "inches away"
FEET_AWAY = "feet away"
YARDS_AWAY = "yards away"
BLOCKS_AWAY = "blocks away"

IGNORE_AGENCIES = ['CANBY', 'CCRIDER', 'CAT', 'YAMHILL']


def reset_logging(level=logging.CRITICAL):
    """ reset logging of all dependencies -- default to queit pretty much everything """ 
    loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    for logger in loggers:
        logger.setLevel(level)


def get_idz(feed_id, stop_id="", agency_id="?"):
    if isinstance(feed_id, dict):
        so = feed_id
        feed_id = so.get("FEED_ID", so.get("feed_id", feed_id))
        stop_id = so.get("STOP_ID", so.get("stop_id", stop_id))
        agency_id = so.get("AGENCY_ID", so.get("agency_id", agency_id))
    return feed_id, stop_id, agency_id


def mk_feed_stop(feed_id, stop_id=""):
    feed_id, stop_id, agency_id = get_idz(feed_id, stop_id)
    return "{}:{}".format(feed_id, stop_id)


def mk_feed_rec(feed_id, stop_id="", agency_id="", use_agency=False):
    feed_id, stop_id, agency_id = get_idz(feed_id, stop_id, agency_id)
    if use_agency:
        ret_val = "{}:{}:{}".format(agency_id, feed_id, stop_id)
    else:
        ret_val = "{}:{}".format(feed_id, stop_id)


def mk_shared_id(stops, min_stops=2, def_val=""):
    ret_val = def_val
    if len(stops) >= min_stops:
        for i, s in enumerate(stops):
            id = mk_feed_rec(s)
            ret_val = "{}{}{}".format(ret_val, "" if i==0 else ",", id)
    return ret_val


def cmp_stop(stop, feed_id, stop_id, agency_id=None, use_agency=False):
    f, s, a = get_idz(stop)
    #import pdb; pdb.set_trace()
    return f == feed_id and s == stop_id and (use_agency is False or agency_id is None or a == agency_id)


def match_stop(stops, feed_id, stop_id, agency_id=None, start_index=0):
    """ finds the first stop match in a list of stops """
    ret_val = None
    for i, s in enumerate(stops):
        if i < start_index:
            continue
        if cmp_stop(s, feed_id, stop_id, agency_id):
            ret_val = s
            break
    return ret_val


def get_active_stops(stops, start_index=0):
    """ loop thru list of stops, returning an array of those not filtered """
    ret_val = []
    for i, s in enumerate(stops):
        if i < start_index:
            continue
        if s.get('filter'):
            continue
        ret_val.append(s)
    return ret_val


def find_stops(shared_stops, target, start_index=0, skip_target=False, check_filter=False):
    """ """
    ret_val = []
    feed_id, stop_id, a = get_idz(target)
    for ss in shared_stops:
        s = match_stop(ss['stops'], feed_id, stop_id, start_index=start_index)
        if s:
            if skip_target and s == target:
                continue
            if check_filter and s.get('filter'):
                continue
            ret_val.append(s)
    return ret_val


def find_shareds(shared_stops, target):
    ret_val = []
    feed_id, stop_id, a = get_idz(target)
    for ss in shared_stops:
        s = match_stop(ss['stops'], feed_id, stop_id)
        if s is None or ss.get('filter'):
            continue
        """
        if s:
            if skip_target and s == target:
                continue
            if s.get('filter'):
                continue
        """
        ret_val.append(ss)
    return ret_val


def strip_agency_id(id):
    "
      will take this id: C-TRAN:CTRAN:4
      and return this: s CTRAN:4
      will only do this if there are more than one colon
    "
    ret_val = id
    if id and id.count(":") > 1:
        parts = id.split(":", 1)
        if len(parts) > 1:
            ret_val = parts[1]
    return ret_val
