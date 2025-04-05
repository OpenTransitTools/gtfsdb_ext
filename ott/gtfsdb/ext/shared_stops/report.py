import os
import inspect
from mako.template import Template
from mako.lookup import TemplateLookup

from ..utils import *

import logging
log = logging.getLogger(__name__)


this_module_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


def generate_report(ss, tmpl = 'report.mako'):
    stops = sorted(ss['shared'], key=lambda x: x['distance'], reverse=True)
    lookup = TemplateLookup(directories=[os.path.join(this_module_dir, 'tmpl'), '/srv/geoserver/gtfsdb_ext/ott/gtfsdb/ext/shared_stops/tmpl', '/srv/geoserver/gtfsdb_ext/ott/gtfsdb/ext/shared_stops/tmpl/'])
    report_tmpl = Template(filename=os.path.join(this_module_dir, 'tmpl', tmpl), lookup=lookup)
    report = report_tmpl.render(stops=stops)
    print(report)


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
