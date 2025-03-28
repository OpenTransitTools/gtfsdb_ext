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
  - sorry for this hack ... if psycopg2-binary is a dependency, poetry tries to build the C source

### run
- poetry run 
- ls blah
