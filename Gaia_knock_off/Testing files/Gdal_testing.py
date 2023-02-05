from Gaia_knock_off.off_road import *
from osgeo import gdal, ogr, osr
from fiona.ogrext import Iterator, ItemsIterator, KeysIterator
from geopandas import GeoDataFrame
import fiona
import os
import pyrosm
import matplotlib

print(gdal.VersionInfo())

output_base_path = 'Gaia_knock_off/OSM_PBF_data'

OSM_PBF_file_generator(place_name ='Leeds', save_location= output_base_path).generate()
