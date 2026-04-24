from gtfsdb import Database
from gtfsdb.scripts import get_args, make_kwargs

ss_url="https://developer.trimet.org/ws/v3/sharedStops?csv=true&appid=8CBD14D520C6026CC7EEE56A9&showshared=true"


def make_cmdline(prog_name):
    parser, kwargs = get_args(prog_name=prog_name, do_parse=False)
    parser.add_argument('--do_parse', '-dp', default=False, action='store_true', help="parse shared-stops locally")
    parser.add_argument('--clear',  '-cl', default=False, action='store_true', help="clear the shared stop columns in *.stops and *.current_stops")
    parser.add_argument('--ss_url', '-su', default=ss_url, help=f"URL of shared-stop definitions {ss_url}")

    args = parser.parse_args()
    if args.schema is None: args.schema = "TRIMET"
    kwargs = make_kwargs(args)

    db = Database(**kwargs)
    return args, db


def shared_stops(prog_name="shared-stops"):
    args, db = make_cmdline(prog_name)

    if args.do_parse:
        from . import process
        ss = process.shared_stops_parser(args.file, db, args.schema)
    else:
        ss = {}
    return args, db, ss
