import os
import inspect
from mako.template import Template
from mako.lookup import TemplateLookup

from .process import cmd_line_get_shared_stops
from ..utils import *

# NOTE: because this generates a report, turn off all logging so it doesn't bleed into the report output
import logging
loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
for logger in loggers:
    #logger.setLevel(logging.DEBUG)
    logger.setLevel(logging.CRITICAL)


this_module_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


def generate_report(ss, src_feed_id, tmpl = 'report.mako'):
    # import pdb; pdb.set_trace()
    #stops = ss['shared']
    stops = sorted(ss['shared'], key=lambda x: x.get('distance', 2112.2112), reverse=True)
    lookup = TemplateLookup(directories=[os.path.join(this_module_dir, 'tmpl'), '/srv/geoserver/gtfsdb_ext/ott/gtfsdb/ext/shared_stops/tmpl', '/srv/geoserver/gtfsdb_ext/ott/gtfsdb/ext/shared_stops/tmpl/'])
    report_tmpl = Template(filename=os.path.join(this_module_dir, 'tmpl', tmpl), lookup=lookup)
    report = report_tmpl.render(src_feed_id=src_feed_id, stops=stops, unsupported=ss.get('unsuppored'), not_active=ss.get('not_active'))
    return report


def create_report():
    args, db, ss = cmd_line_get_shared_stops()
    report = generate_report(ss, args.schema)
    print(report)
