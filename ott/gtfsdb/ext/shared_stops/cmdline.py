from gtfsdb import Database
from gtfsdb.scripts import get_args


def make_cmdline(prog_name):
    args, kwargs = get_args(prog_name=prog_name)
    if args.schema is None:
        args.schema = "TRIMET"

    db = Database(**kwargs)
    return args, db


def shared_stops(prog_name="shared-stops"):
    args, db = make_cmdline(prog_name)

    from . import process
    ss = process.shared_stops_parser(args.file, db, args.schema)
    return args, db, ss
