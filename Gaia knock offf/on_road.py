import googlemaps
from datetime import datetime
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import json




Local_dev = True

if Local_dev:

    google_api_key = "AIzaSyAxwIx5PGLy3P5ta6QpUy9TkJFSJOcGtFQ"

else:
    google_api_key = input("")


gmaps = googlemaps.Client(key=google_api_key)

class directions(object):

    def __init__(self,start, end_destination, mode = "driving"):

        self.start = start
        self.end_destination = end_destination
        self.mode = mode
        self.gmaps = googlemaps.Client(key=google_api_key)
        self.now = datetime.now()
        
    def google_directions(self):
        self.gmaps
        now = self.now
        directions_result = self.gmaps.directions(self.start, self.end_destination, mode=self.mode, departure_time = now)

        return directions_result

    def direction_data(self):

        direction_data = self.google_directions()[0]
        keys_relevant = ['bounds', 'legs', 'warnings', 'waypoint_order']

        bounds_data = direction_data[keys_relevant[0]]
        legs_data = direction_data[keys_relevant[1]]
        warnings_data = direction_data[keys_relevant[2]]
        waypoint_order_data = direction_data[keys_relevant[3]]

        return bounds_data, legs_data, warnings_data, waypoint_order_data

    def legs_data(self):

        bounds_data, legs_data, warnings_data, waypoint_order_data = self.direction_data()

        return legs_data[0]

    def bound_data(self):

        bounds_data, legs_data, warnings_data, waypoint_order_data = self.direction_data()

        return bounds_data

    def steps_data(self):

        legs_data = self.legs_data()


        print(type(legs_data))
        print(legs_data["steps"])
        print(type(legs_data["steps"]))
        print(len(legs_data["steps"]))

        '''
        debug this 
        '''

        steps_data = legs_data["steps"]


        return steps_data





start = 'Sydney Town Hall'
end = 'Parramatta, NSW'
mode = "driving"

modes = ["driving", "walking", "bicycling", "transit"]

# direction = directions(start = start, end_destination = end, mode = mode).google_directions()

direction = directions(start = start, end_destination = end, mode = mode)
keys_important = "distance duration end_location html_instructions start_location travel_mode".split()
step_data = direction.steps_data()

print(step_data)

for data in step_data:

    print(data)
    print("\n ")

