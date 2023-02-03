from Gaia_knock_off.on_road import *
import requests

'''
set up roads API infastructure

find patch of area defined by, nearest road being 10km away from nearest road within
distance start_distance to end distance radius

find 

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

