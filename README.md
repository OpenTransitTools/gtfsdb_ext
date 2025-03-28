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
- poetry install
- poetry run pip3 install psycopg2-binary 
  - this last step might be needed if you run things and get a psycopg2 missing dependency error
  - appologies for this hack: having psycopg2-binary as a dependency, poetry tries to build the C source

### applications
- poetry run shared_stops_report
  - shared stop report shows stop relationships between 
  - show blah...

- poetry run shared_stops_populate
  - populate the gtfsdb stops.shared_stops column

- poetry run gtfsdb-load -OR- gtfsdb-current-load
  - the same cmd-line apps from the gtfsdb project (just via this project / poetry)
  - see https://github.com/OpenTransitTools/gtfsdb?tab=readme-ov-file#install-from-source-via-github-if-you-want-the-latest-code-
