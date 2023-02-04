from osgeo import gdal, ogr, osr
from fiona.ogrext import Iterator, ItemsIterator, KeysIterator
from geopandas import GeoDataFrame
import fiona
import os

# os.add_dll_directory()

gdal.VersionInfo()

# import pyrosm