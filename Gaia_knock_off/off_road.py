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

        # url = "https://roads.googleapis.com/v1/nearestRoads?points=60.170880%2C24.942795%7C60.170879%2C24.942796%7C60.170877%2C24.942796&key=YOUR_API_KEY"

        # base_url = "https://roads.googleapis.com/v1/nearestRoads?"

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

# 60.170880,24.942795|60.170879,24.942796|60.170877,24.942796

pointers = [('60.170880','24.942795'),('60.170879','24.942796'),('60.170877','24.942796')]

# api_key = "AIzaSyAxwIx5PGLy3P5ta6QpUy9TkJFSJOcGtFQ"
#
#
# text = nearest_roads_api(pointers = pointers, api_key = api_key).text()

# print(text)


'''
need an algorithm to get pbf data into odd road data
go for Resources.txt

'''
