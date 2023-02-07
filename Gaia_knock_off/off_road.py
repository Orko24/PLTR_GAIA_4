from Gaia_knock_off.on_road import *
import requests
from osgeo import gdal, ogr, osr
from fiona.ogrext import Iterator, ItemsIterator, KeysIterator
from geopandas import GeoDataFrame
import fiona
import os
import pyrosm
import matplotlib
from pathlib import Path

'''
set up roads API infastructure

find patch of area defined by, nearest road being 10km away from nearest road within
distance start_distance to end distance radius given by the user

find list of roads that border the area, 

find road closet to starting point
find road closet to ending point
get 2 on road directions

link to the via patch

off road instructions 

'''



BASE_DIR = Path(__file__).resolve().parent.parent

class nearest_roads_api(object):

    def __init__(self, pointers, payload = {}, headers = {}, api_key = None):
        '''
        :cvar
        pointers: [('lat','lng'),...]
        payload: dictionary
        headers: dictionary
        api_key: google directions api key

        :return
        '''
        self.pointers = pointers
        self.payload = payload
        self.headers = headers
        self.api_key = api_key

    def pointers_string(self):

        pointers = self.pointers
        pointer_string = "points="
        for lat, lng in pointers:

            pointer_string = pointer_string + "{},{}|".format(lat,lng)

        pointer_string = pointer_string[:-1]

        pointer_string.replace(",", "%2C")
        pointer_string.replace("|", "%7C")

        return pointer_string

    def url(self):

        base_url = "https://roads.googleapis.com/v1/nearestRoads?"
        parameters = self.pointers_string()

        string = "{}{}&key={}".format(base_url, parameters, self.api_key)

        return string

    def response(self):

        url = self.url()
        response = requests.request("GET", url, headers=self.headers, data=self.payload)
        return response

    def text(self):
        response = self.response()

        return response.text


class OSM_PBF_file_generator(object):
    
    def __init__(self,place_name, save_location,update=True):

        self.place_name = place_name
        self.save_location = save_location
        self.update = update

    def generate(self):

        dir_path = os.path.join(BASE_DIR, self.save_location)
        file_name = "{}.osm.pbf".format(self.place_name)
        full_file_path = os.path.join(dir_path,file_name)

        if not self.update:
            if os.path.exists(full_file_path):
                print("exists")
                return full_file_path

        file_path = pyrosm.get_data(self.place_name, directory=dir_path, update=self.update)
        return file_path

'''
PSUEDO ALGO FOR OFF ROAD DIRECTIONS ARE IN THE FOLLOWING

based on start and end destination, check which geographic location 
based on lattitude and longitude 

the and try to box it in on the osm.pbf file and feed it into 

from offroad_routing import Geometry

filename = "../maps/user_area.osm.pbf"
bbox = [34, 59, 34.2, 59.1]
geom = Geometry.parse(filename=filename, bbox=bbox)

https://denikozub.github.io/Offroad-routing-engine/#installation

From here an off road route can be generated 

You may use stopping points based on longitude and latitude and feed into the on_road API built

that will give you the instructions via text format
'''




