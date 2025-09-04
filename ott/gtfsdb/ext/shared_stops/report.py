import os
import inspect
from mako.template import Template
from mako.lookup import TemplateLookup

from .process import cmd_line_get_shared_stops
from ..utils import *

reset_logging() # NOTE: turn off all logging so it doesn't bleed into the report output
this_module_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


def generate_report(ss, src_feed_id, tmpl = 'report.mako'):
    # import pdb; pdb.set_trace()
    stops = sorted(ss['shared'], key=lambda x: x.get('distance', 2112.2112), reverse=True)
    # note: the this_mod_dir / tmpl should find the mako stuff here, but also hard code a couple svr directories for good measure in case we want to run things from outside this project
    lookup = TemplateLookup(directories=[os.path.join(this_module_dir, 'tmpl'), '/srv/geoserver/gtfsdb_ext/ott/gtfsdb/ext/shared_stops/tmpl', '/srv/geoserver/gtfsdb_ext/ott/gtfsdb/ext/shared_stops/tmpl/'])
    report_tmpl = Template(filename=os.path.join(this_module_dir, 'tmpl', tmpl), lookup=lookup)
    report = report_tmpl.render(src_feed_id=src_feed_id, stops=stops, unsupported=ss.get('unsupported'), not_active=ss.get('not_active'))
    return report


def echo_shared_stops():
    args, db, ss = cmd_line_get_shared_stops('echo-shared-stops')
    print(args)
    print()
    print(ss.get('unsupported'))
    print(ss.get('not_active'))
    print()
    for s in ss.get('shared'):
        print(s)


def create_report():
    args, db, ss = cmd_line_get_shared_stops('shared-stops-report')
    report = generate_report(ss, args.schema)
    print(report)

