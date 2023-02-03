from Gaia_knock_off.on_road import *
import requests

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

class nearest_roads_api(object):

    def __init__(self, pointers,payload, headers, api_key = None):
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

        # url = "https://roads.googleapis.com/v1/nearestRoads?points=60.170880%2C24.942795%7C60.170879%2C24.942796%7C60.170877%2C24.942796&key=YOUR_API_KEY"

        base_url = "https://roads.googleapis.com/v1/nearestRoads?"

        pointers = self.pointers

        pointer_string = "points="
        for lat, lng in pointers:

            pointer_string =

