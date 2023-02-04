from osgeo import gdal, ogr, osr
from fiona.ogrext import Iterator, ItemsIterator, KeysIterator
from geopandas import GeoDataFrame
import fiona
import os
import pyrosm
import matplotlib

print(gdal.VersionInfo())

