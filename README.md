# A Web interface for OCO2 data

## Run the code
* install requirements (Python 3.3+ required)
* run python config.py
* download files from NASA using the script in files/
* run main.py to dump data from files to db

## To-do
* [PostGRE-PostGIS](http://postgis.net/) support
* Write test queries
* Design the REST interface
* Set up the Web server


### PostGIS How-tos
PostGIS is a quite wide extension for PostGRE: check the [features](http://www.postgis.us/downloads/postgis21_cheatsheet.html).
Full manual [here](http://postgis.net/docs/manual-dev).
It makes possible calculations over planar (geometry) or ellipsoidal (geography) spatial data types. In latest versions of PostGRE it can be activated as EXTENSION.

#### create a PostGIS database
From psql command line:
```
CREATE DATABASE gisdb;
\connect gisdb;
-- Enable PostGIS (includes raster)
CREATE EXTENSION postgis;
-- Enable Topology
CREATE EXTENSION postgis_topology;
-- Enable PostGIS Advanced 3D 
-- and other geoprocessing algorithms
CREATE EXTENSION postgis_sfcgal;
-- fuzzy matching needed for Tiger
CREATE EXTENSION fuzzystrmatch;
-- rule based standardizer
CREATE EXTENSION address_standardizer;
-- example rule data set
CREATE EXTENSION address_standardizer_data_us;
-- Enable US Tiger Geocoder
CREATE EXTENSION postgis_tiger_geocoder;
-- routing functionality
CREATE EXTENSION pgrouting;
-- spatial foreign data wrappers
CREATE EXTENSION ogr_fdw;

-- LIDAR support
CREATE EXTENSION pointcloud;
-- LIDAR Point cloud patches to geometry type cases
CREATE EXTENSION pointcloud_postgis;
```

#### create indexes
```
CREATE INDEX idx_table_geom
ON table
USING gist(geometry_field);


CREATE INDEX idx_table_town
ON table
USING btree(some_field);
```

#### create a geometry column in PostGIS 2:
```
-- Add a point using the old constraint based behavior
SELECT AddGeometryColumn ('my_schema','my_spatial_table','geom_c',4326,'POINT',2, false);
```
Example: 

* Create a geometry column using the SRID 4326 (using PostGIS 2.0 syntax), to hold the GIS object:
```
ALTER TABLE table ADD COLUMN geom geometry(POINT,4326);
```
* Update the geometry column with the latitude and longitude of each point:
```
UPDATE table SET geom = ST_SetSRID(ST_MakePoint(longitude,latitude),4326);
```
* And create a spatial index:
```
CREATE INDEX idx_table_geom ON table USING GIST(geom);
```

#### create a geography column
```
CREATE TABLE testgeog(gid serial PRIMARY KEY, the_geog geography(POINT,4326) );
```