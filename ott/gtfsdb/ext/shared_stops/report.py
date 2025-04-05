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
    report = report_tmpl.render(stops=stops, unsupported=ss.get('unsuppored'), no_stop=ss.get('no_stop'))
    print(report)
