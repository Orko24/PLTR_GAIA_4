import googlemaps
from datetime import datetime
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import json
import html
from bs4 import BeautifulSoup




Local_dev = True

class directions(object):

    def __init__(self,start, end_destination, mode = "driving",
                 google_api_key = None):

        self.start = start
        self.end_destination = end_destination
        self.mode = mode
        self.google_api_key = google_api_key
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
        '''
        debug this 
        '''

        steps_data = legs_data["steps"]


        return steps_data


    def step_instructions_data(self):

        '''
        nested loop dictionary

        keys for the first dictionary should be, the number of steps and what values should go so

        {1: {distance data, duration data, html_instructions, manuever, start_location, travel mode} 2: {...} ... }


        reason track the direction per step, this will allow detailed data analysis and for off_road

        the detection of patches, try to get geographic name of patch

        :return:
        '''

        # relevant_data_keys = ['distance', 'duration', 'end_location', 'html_instructions',
        #                  'maneuver', 'start_location', 'travel_mode']

        relevant_data_keys = ['distance', 'duration', 'end_location',
                              'html_instructions', 'start_location',
                              'travel_mode']

        steps_data = self.steps_data()

        filtered_data = {}

        for i in range(len(steps_data)):

            data = steps_data[i]
            relevant_data = {}

            # print(type(data))
            # print(data.keys())

            for key in relevant_data_keys:
                relevant_data[key] = data[key]

            filtered_data[i] = relevant_data

        return filtered_data, relevant_data_keys

    def filtered_instructions_data(self):

        '''
        filter logic, what you want is the data in a sequenced list based on index position
        where index position matches step number
        so you want

        distance : [{value 1}, {value 2}....]
        duration : [{value 1}, .....]

        .....

        '''

        filtered_data, relevant_data_keys = self.step_instructions_data()

        filter_keys = ['distance', 'duration', 'end_location', 'html_instructions', 'start_location']

        filtered_data_keys = list(filtered_data.keys())

        structured_data = {}


        for key in filter_keys:
            temp_data = []
            for prime_key in filtered_data_keys:
                data = filtered_data[prime_key][key]
                temp_data.append(data)
            structured_data[key] = temp_data


        return structured_data, filter_keys

    '''
    HTML instructions processing
    '''

    def directions_full(self):

        structured_data, filter_keys = self.filtered_instructions_data()
        return structured_data['html_instructions']

    def directions_text(self):

        directions_full = self.directions_full()

        instructions_lst = []
        instructions_string = ""

        for instructions in directions_full:

            soup = BeautifulSoup(instructions, 'html.parser')
            # print(soup.prettify())
            text = soup.get_text()
            instructions_lst.append(text)
            instructions_string = instructions_string + "{}\n".format(text)


        return instructions_lst, instructions_string

    def distance_full(self):

        structured_data, filter_keys = self.filtered_instructions_data()
        return structured_data['distance']

    def distance_data(self):

        distance_full = self.distance_full()
        raw_data = []
        distance_lst = []
        distance_vals = []
        
        for data in distance_full:

            # print(data['text'].split())
            
            datum = data['text'].split()
            # raw_data.append(datum)
            datum[0] = float(datum[0])
            if datum[1] == "m":
                datum[0] = datum[0]/1000
                datum[1] = "km"

            distance_lst.append(datum)
            distance_vals.append(datum[0])

            # print(datum)
            
        # print(sum(distance_vals))
        
        full_distance = str(sum(distance_vals)) + "km"

        for data in distance_full:

            datum = data['text'].split()
            raw_data.append(datum)

        full_distance = str(sum(distance_vals)) + "km"
        return distance_lst, full_distance, raw_data

    def distance_lst(self):

        distance_lst, full_distance, raw_data = self.distance_data()
        return distance_lst

    def full_distance(self):

        distance_lst, full_distance, raw_data = self.distance_data()
        return full_distance

    def raw_data(self):

        distance_lst, full_distance, raw_data = self.distance_data()
        return raw_data

    def duration_data(self):

        'duration'

        structured_data, filter_keys = self.filtered_instructions_data()

        duration_data = structured_data['duration']
        return duration_data

    def raw_duration_data_processing(self):

        duration_full = self.duration_data()
        raw_data = []


        for data in duration_full:

            datum = data['text'].split()
            # print(datum)
            raw_data.append(datum)

        return raw_data

    def filtered_duration_data(self):

        raw_data = self.raw_duration_data_processing()

        durations = []

        for duration, formats in raw_data:

            duration = int(duration)

            if formats == "hr" or formats == "hrs" or formats == "hours":

                duration = duration * 60
                formats = "min"

            durations.append(duration) #<--- labelled in minutes data

        full_time = sum(durations)

        if full_time > 60:
            q, r = divmod(full_time, 60)
            display = "{}hr {}mins".format(q,r)

        else:
            display = "{}mins".format(full_time)

        return raw_data, display


class direction_data_filtered(object):

    def __init__(self, start, end_destination, mode="driving",
                 google_api_key= None):
        self.start = start
        self.end_destination = end_destination
        self.mode = mode
        self.google_api_key = google_api_key
        self.gmaps = googlemaps.Client(key=google_api_key)
        self.now = datetime.now()

    def direction_data(self):
        direction_data = directions(start = self.start, end_destination = self.end_destination,
                                    mode = self.mode, google_api_key = self.google_api_key)

        return direction_data

    def filtered_data(self):

        direction_data = self.direction_data()
        html_data = direction_data.directions_full()
        instructions_lst, instructions_string = direction_data.directions_text()
        distance_data = direction_data.distance_data()
        duration_data = direction_data.filtered_duration_data()

        return html_data, instructions_lst, instructions_string, distance_data, duration_data

    def directions_lat_long_data(self):
        direction_data = self.direction_data()

        # ['distance', 'duration', 'end_location', 'html_instructions', 'start_location']

        structured_data, filter_keys = direction_data.filtered_instructions_data()

        end_location_data_html = structured_data[filter_keys[2]]
        start_location_data_html = structured_data[filter_keys[4]]

        return start_location_data_html,end_location_data_html

    def route_geocode(self):
        '''
        full piece of encoded route and geo data

        :return:
        '''
        route_data = self.filtered_data()
        geo_data = self.directions_lat_long_data()

        return route_data, geo_data

    def route_data_readable(self):
        '''
        encoded route and geo data into one data structure for processing

        :return:
        '''
        route_data, geo_data = self.route_geocode()

        html_data, instructions_lst, instructions_string, distance_data, duration_data = route_data

        distance_lst, full_distance, raw_data_distance = distance_data
        time_lst, display = duration_data

        instructions_data = []


        for i in range(len(instructions_lst)):

            '''
            fix this tmmr
            '''

            # print(instructions_lst[i], distance_lst[i], time_lst[i])

            '''
            keep it in data array structure for further maninpuation by adding lattitude and longitudes
            '''

            instructions_data.append([instructions_lst[i], distance_lst[i], time_lst[i]])

        return instructions_data

    def geo_data_route(self):

        instructions_data = self.route_data_readable()
        route_data, geo_data = self.route_geocode()

        # print(geo_data)
        # print(instructions_data)


        '''
        geo data processing
        '''

        start_location_data_html, end_location_data_html = geo_data

        latitude_data_start = []
        longitude_data_start = []

        latitude_data_end = []
        longitude_data_end = []

        for data_pos in range(len(start_location_data_html)):

            data_start = start_location_data_html[data_pos]
            data_keys_start = list(data_start.keys())
            lat_key_start, lng_key_start = data_keys_start[0], data_keys_start[1]

            latitude_data_start.append([lat_key_start, data_start[lat_key_start]])
            longitude_data_start.append([lng_key_start,data_start[lng_key_start]])

            data_end = end_location_data_html[data_pos]
            data_keys_end = list(data_end.keys())
            lat_key_end, lng_key_end = data_keys_end[0], data_keys_end[1]

            latitude_data_end.append([lat_key_end, data_start[lat_key_end]])
            longitude_data_end.append([lng_key_end, data_start[lng_key_end]])


        # geo_code_route_data = []

        # for pos in range(len(instructions_data)):
        #
        #     print(latitude_data_start[pos], longitude_data_start[pos])
        #     print(latitude_data_end[pos], longitude_data_end[pos])
        #     print(instructions_data[pos])

        return instructions_data, latitude_data_start, longitude_data_start, latitude_data_end, longitude_data_end

    def instructions_route_geo(self):

        instructions_data, latitude_data_start, longitude_data_start, latitude_data_end, longitude_data_end = self.geo_data_route()

        instruction_route_data = []
        instruction_route_geo_data = []

        for element in instructions_data:

            instruction = element[0]
            distance_ = element[1]
            duration_ = element[2]

            instruction_string = "{} (distance: {}{} duration:{}{})".format(instruction, distance_[0],distance_[1],
                                                         duration_[0],duration_[1])

            instruction_route_data.append(instruction_string)

        # data_time_distance = ""
        # for instruction_route in instruction_route_data:
        #
        #     data_time_distance = data_time_distance + "{}\n ".format(instruction_route)

        geo_code_data_string = ""
        for geo_code_pos in range(len(instruction_route_data)):

            geo_code_data = instruction_route_data[geo_code_pos]
            geo_code_string = "{} (start geocode data: {}, end geocode data: {}".format(geo_code_data,
                                (latitude_data_start[geo_code_pos], longitude_data_start[geo_code_pos]),
                                (latitude_data_end[geo_code_pos], longitude_data_end[geo_code_pos]))
            # geo_code_data_string = geo_code_data_string + "{}\n ".format(geo_code_string)

            instruction_route_geo_data.append(geo_code_string)

        return instruction_route_data, instruction_route_geo_data

    def instructions(self):

        instruction_route_data, instruction_route_geo_data = self.instructions_route_geo()

        route_data, geo_data = self.route_geocode()
        html_data, instructions_lst, instructions_string, distance_data, duration_data = route_data

        instruction_route_text = ""
        instruction_route_geo_data_text = ""

        for element in instruction_route_data:

            instruction_route_text = instruction_route_text + "{}\n".format(element)

        for element in instruction_route_geo_data:
            instruction_route_geo_data_text = instruction_route_geo_data_text + "{}\n".format(element)

        # print(instruction_route_text)
        # print(instruction_route_geo_data_text)
        # print(instructions_string)
        # print(distance_data)
        # print(duration_data)

        full_distance = distance_data[1]
        full_duration = duration_data[1]

        text_data = [instructions_string, instruction_route_text, instruction_route_geo_data_text]

        return text_data, full_distance, full_duration

class route_filtered_data(object):

    def __init__(self, start, end_destination, mode="driving",
                 google_api_key= None):
        self.start = start
        self.end_destination = end_destination
        self.mode = mode
        self.google_api_key = google_api_key
        self.gmaps = googlemaps.Client(key=google_api_key)
        self.now = datetime.now()

    def direction_data(self):

        direction_data = direction_data_filtered(start= self.start, end_destination=self.end_destination,
                                                 mode = self.mode, google_api_key= self.google_api_key)
        return direction_data

    def text(self):

        direction_data = self.direction_data()
        text_data, full_distance, full_duration = direction_data.instructions()
        
        data_full = []
        
        for text in text_data:
            # print(text_data)

            # print("text is the following")
            # print(text)
            # print(full_distance)
            # print(full_duration)

            text_data_full = "{}\nroute full distance: {}\nroute full duration: {}".format(text, full_distance, full_duration)

            # print(text_data_full)

            data_full.append(text_data_full)


        return data_full

    def text_data(self):

        direction_data = self.direction_data()
        text_data, full_distance, full_duration = direction_data.instructions()
        return text_data, full_distance, full_duration


