from ..utils import *

import logging
log = logging.getLogger(__name__)


def generate_report(ss):
    for s in ss['shared']:
        print(s)



def Xgenerate_report(ss):
    url = "https://rtp.trimet.org/rtp/#/schedule"

    print("There are {} shared stops defined in TRANS.".format(len(ss['src'])))

    print("\nCould not find a matching stop for the following ({}):".format(len(ss[NOT_FOUND])))
    for s in ss[NOT_FOUND]:
        #print(s)
        print("   {}: {}/{}".format(s['share'], url, s['feed_stop']))

    for d in [BLOCKS_AWAY, YARDS_AWAY, FEET_AWAY, INCHES_AWAY]:
        print("\nThese stops are {} from the target stop ({}):".format(d, len(ss[d])))
        for s in ss[d]:
            print("   {}: {}/{}".format(s['share'], url, strip_agency_id(s['src'])))
            #print(s)
