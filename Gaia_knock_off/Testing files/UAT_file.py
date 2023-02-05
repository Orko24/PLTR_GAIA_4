from Gaia_knock_off.off_road import *

# from Gaia_knock_off.on_road import *
#
#
# start = 'Sydney Town Hall'
# end = 'Parramatta, NSW'
# mode = "driving"
# modes = ["driving", "walking", "bicycling", "transit"]
# api_key = "AIzaSyAxwIx5PGLy3P5ta6QpUy9TkJFSJOcGtFQ"


# route_info = route_filtered_data(start = start, end_destination = end, mode = mode, google_api_key = api_key)
#
# data_full = route_info.text()
#
# for text in data_full:
#
#     print(text)

# # start by importing your packages
# import fiona
# # import pyrosm
# # import matplotlib
#
# # 60.170880,24.942795|60.170879,24.942796|60.170877,24.942796
#
# pointers = [('60.170880','24.942795'),('60.170879','24.942796'),('60.170877','24.942796')]
#
# # api_key = "AIzaSyAxwIx5PGLy3P5ta6QpUy9TkJFSJOcGtFQ"
# #
# #
# # text = nearest_roads_api(pointers = pointers, api_key = api_key).text()
#
# # print(text)

'''
need an algorithm to get pbf data into odd road data
go for Resources.txt

'''
# available_places = pyrosm.data.available
# print(available_places.keys())
# print(available_places)
# print('Leeds available from providers:','Leeds' in available_places['cities'])

output_base_path = 'Gaia_knock_off/OSM_PBF_data'
# dir_path = os.path.join(BASE_DIR, output_base_path)

# Gets data from pyrosm providers (BBBike or Geofabrik) and stores in /temp directory - file can be saved to a user specified
# location with additional argument directory i.e. get_data(place_name, directory='save_path')
# place_name = 'Leeds'
# file_path = pyrosm.get_data(place_name, directory= dir_path)
# print('Data downloaded to:', file_path)


OSM_PBF_file_generator(place_name ='Leeds', save_location= output_base_path).generate()

