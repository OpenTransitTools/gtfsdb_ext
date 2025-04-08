from gtfsdb import Database
from gtfsdb.util import get_csv
from gtfsdb.scripts import get_args

from .. import query
from ..utils import *

reset_logging()

def update_db(shared_stops, db, src_feed_id):
#    print(shared_stops)
    for s in shared_stops.get('shared'):
#        print(s)
        continue

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
        'stops': stops,
        'filter': False,
        'shared_id': ""
    }
    return ret_val


def make_skips(stop_recs, start=0):
    """ utility to build dict that counts the feed/stop pairs """
    skips = {}
    for s in stop_recs:
        fs = mk_feed_stop(s)
        if skips.get(fs) is None:
            skips[fs] = start
        else:
            skips[fs] = skips[fs] + 1
    return skips


def make_counts(stop_recs, not_active, start=1):
    """ utility to build dict of stop_id (repeated) counts """    
    counts = {}
    for s in stop_recs:
        fs = s['STOP_ID']
        if fs in not_active:
            continue
        if counts.get(fs) is None:
            counts[fs] = start
        else:
            counts[fs] = counts[fs] + 1
    return counts


def shared_stops_parser(csvfile, db, src_feed_id):
    unsuppored = {}
    not_active = {}

    ret_val = {
        'unsuppored': unsuppored,
        'not_active': not_active,
        'shared': []
    }

    # step 1: grab the csv file, and then query the db and append stop and nearest stop datak
    stop_recs = build_shared_stops_data(csvfile, db, src_feed_id)

    # step 2: make skips (used in step 3) to determine if we have repeat stops, and need a the next nearest stop
    skips = make_skips(stop_recs)
    duplicates = {}

    # step 2: run thru stop data to build up stops list, etc...
    for s in stop_recs:
        #import pdb; pdb.set_trace()
        fs = mk_feed_stop(s)
        src = s.get('src_stop')
        agy = s.get('agencies')
        if agy:
            if src:                
                z = db_rec_to_shared_stop(s, skips[fs])
                x = query.to_stop_dict(src[0], feed_id="TRIMET", distance=z.get('distance'))
                z['stops'].insert(0, x)
                ret_val['shared'].append(z)
                skips[fs] = skips[fs] - 1  # decriment skips, so that we pick up nearer stops on next hits

                # mark duplicate stops
                for zs in z['stops']:
                    id = mk_feed_stop(zs)
                    if id in duplicates:
                        zs['duplicate'] = True
                        duplicates[id]['duplicate'] = True
                    duplicates[id] = zs
            else:
                not_active[s.get('STOP_ID')] = s['FEED_ID']
        else:
            unsuppored[s.get('AGENCY_DESC')] = s.get('AGENCY_DESC')

    # step 3 filter distant and duplicate stops (part A)
    for s in ret_val['shared']:
        if s.get('distance') > 100.0:
            # 3a: if a stop is over 100 meters, filter it (simple)
            s['filter'] = True
            s['stops'][0]['filter'] = True
        elif not s['filter']:
            # 3b: filter duplicate source stops that are over 30 meters from each other 
            if s['stops'][0].get('duplicate') and not s['stops'][0].get('filter'):
                tgt = s['stops'][0]
                dups = find_stops(ret_val['shared'], tgt, check_filter=True)
                ld = len(dups)
                if ld > 1:
                    short = min(dups, key=lambda x: x.get('distance'))
                    max_dist = short.get('distance') + 30.0
                    for x in dups:
                        if x.get('distance') > max_dist:
                            x['filter'] = True
            elif s['stops'][1].get('duplicate') and not s['stops'][1].get('filter'):
                # 3c: find the closest duplicate, and filter out the other (further away) stops that matched
                tgt = s['stops'][1]
                dups = find_stops(ret_val['shared'], tgt, start_index=1, check_filter=True)
                ld = len(dups)
                if ld > 1:
                    short = min(dups, key=lambda x: x.get('distance'))
                    for x in dups:
                        if x != short:
                            x['filter'] = True

    # 4: set the shared stop elements
    seen = {}
    for s in ret_val['shared']:
        tgt = s['stops'][0]
        tid = mk_feed_stop(tgt)

        # step a: make sure we have not seen this stop, and it's not filtered
        if s['filter'] or tgt.get('filter'): # or seen.get(tid):
            continue

        # step b: find all the stops for this target
        stopz = [tgt]
        if tgt.get('duplicate'):
            dups = find_shareds(ret_val['shared'], tgt)
            for d in dups:
                acts = get_active_stops(d['stops'], start_index=1)
                stopz.extend(acts)
            if len(stopz) > 1:
                seen[tid] = tid
        else:
            acts = get_active_stops(s['stops'], start_index=1)
            if len(acts) >= 1:
                seen[tid] = tid
                stopz.extend(acts)

        # step c: make the <agency>:<feed>:<stop>,<agenc... string and assign to stops
        id = mk_shared_id(stopz)
        s['shared_id'] = id
 
    return ret_val


def cmd_line_get_shared_stops():
    args, kwargs = get_args()
    if args.schema is None:
        print("WARNING: you probably need to define '-s <scehma>' on the cmdline for the query agency.  Will default to 'TRIMET'")
        args.schema = "TRIMET"

    db = Database(**kwargs)
    ss = shared_stops_parser(args.file, db, args.schema)
    return args, db, ss


def update_shared_stops():
    args, db, ss = cmd_line_get_shared_stops()
    update_db(ss, db, args.schema)
