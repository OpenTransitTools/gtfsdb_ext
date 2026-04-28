import os
import inspect
from mako.template import Template
from mako.lookup import TemplateLookup

from . import cmdline
from . import process
from ..utils import reset_logging

reset_logging()  # NOTE: turn off all logging so it doesn't bleed into the report output
this_module_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


def generate_report(ss, src_feed_id, tmpl='report.mako'):
    # import pdb; pdb.set_trace()
    stops = sorted(ss['shared'], key=lambda x: x.get('distance', 2112.2112), reverse=True)
    # note: the this_mod_dir / tmpl should find the mako stuff here, but also hard code a couple svr directories for good measure in case we want to run things from outside this project
    lookup = TemplateLookup(directories=[os.path.join(this_module_dir, 'tmpl'), '/srv/geoserver/gtfsdb_ext/ott/gtfsdb/ext/shared_stops/tmpl', '/srv/geoserver/gtfsdb_ext/ott/gtfsdb/ext/shared_stops/tmpl/'])
    report_tmpl = Template(filename=os.path.join(this_module_dir, 'tmpl', tmpl), lookup=lookup)
    report = report_tmpl.render(src_feed_id=src_feed_id, stops=stops, unsupported=ss.get('unsupported'), not_active=ss.get('not_active'))
    return report


def create_report():
    args, db = cmdline.make_cmdline('shared-stops-report')
    ss = process.shared_stops_parser(args.file, db, args.schema)
    report = generate_report(ss, args.schema)
    print(report)
    if not args.do_parse:
        # note: if here, then maybe warn that the shared stops were parsed locally
        pass


def create_csv():
    args, db = cmdline.make_cmdline('shared-stops-csv')
    ss = process.shared_stops_parser(args.file, db, args.schema)
    csv = generate_report(ss, args.schema, "csv.mako")
    print(csv)
    if not args.do_parse:
        # note: if here, then maybe warn that the shared stops were parsed locally
        pass


def echo_shared_stops():
    args, db = cmdline.make_cmdline('echo-shared-stops')
    print(args)
    print()

    stops = []
    if args.do_parse:
        ss = process.shared_stops_parser(args.file, db, args.schema)
        print(ss.get('unsupported'))
        print(ss.get('not_active'))
        stops = ss.get('shared', [])
    else:
        from . import service
        stops = service.call_service(args.ss_url)

    print()
    for s in stops:
        print(s)
    print()
