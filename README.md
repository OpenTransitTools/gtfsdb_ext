# gtfsdb_ext
# ----------
about: post-processing routines and extensions for gtfsdb, especially for multiple agency 
goals: keep the gtfsdb project clean (going to need a refactoring there as it's gotten a bit messy), 
       moving all 'customizations' (and hacks) to the gtfsdb_ext project.
notes: 
 - Postgres as the backend database tied to this project currently (2025)
 - python 3.6 or greater

# installation 
- pip install poetry
- git clone https://github.com/OpenTransitTools/gtfsdb_ext.git
- cd gtfsdb_ext
- poetry install
  - if install fails on psycopg2, then do the following:
  - poetry run pip3 install psycopg2-binary
  - (sorry for the hack ... not sure of another way to make poetry do what pip does)
  - (note: psycopg 3.0.18 is the last py 3.6 supported version)

# run
- poetry run json2locs
- ls *.json
