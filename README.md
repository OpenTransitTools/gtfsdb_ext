# gtfsdb_ext
----------
**about**: post-processing routines and extensions for gtfsdb, especially for blending multiple agencies across a varierty of feeds

**goals**: keep the gtfsdb project clean (going to need a refactoring there as it's gotten a bit messy), moving all 'customizations' (and hacks) to the gtfsdb_ext project.

**notes**: 
 - Postgres is the only database supported by this project currently (2025)
   so much so, that pg is tied tightly in the poetry install
 - python 3.6 or greater

### installation 
- pip install poetry
- git clone https://github.com/OpenTransitTools/gtfsdb_ext.git
- cd gtfsdb_ext
- git update-index --assume-unchanged poetry.lock
- poetry install
- poetry run pip3 install psycopg2-binary 
  - this last step might be needed if you run things and get a psycopg2 missing dependency error
  - appologies for this hack: having psycopg2-binary as a dependency, poetry tries to build the C source

### applications
 - shared-stops report
   - show the multi-agency stop relationships, where multiple agencies (and multiple GTFS feeds) serve the same physical location (as well as probably sharing the same signage)
   - poetry run shared-stops-report -s TRIMET -d postgresql://ott:ott@127.0.0.1:5432/ott ott/gtfsdb/ext/shared_stops/data/shared_stops.csv > report.html

 - shared-stops populate
   - populate the gtfsdb stops.shared_stops column
   - poetry run shared_stops_populate -d postgresql://ott:ott@127.0.0.1:5432/ott ott/gtfsdb/ext/shared_stops/data/shared_stops.csv

 - poetry run gtfsdb-load -OR- gtfsdb-current-load
   - the same cmd-line apps from the gtfsdb project (just via this project / poetry)
   - see https://github.com/OpenTransitTools/gtfsdb?tab=readme-ov-file#install-from-source-via-github-if-you-want-the-latest-code-
