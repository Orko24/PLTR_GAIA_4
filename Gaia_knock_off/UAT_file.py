from Gaia_knock_off.on_road import *


start = 'Sydney Town Hall'
end = 'Parramatta, NSW'
mode = "driving"
modes = ["driving", "walking", "bicycling", "transit"]
api_key = "AIzaSyAxwIx5PGLy3P5ta6QpUy9TkJFSJOcGtFQ"


route_info = route_filtered_data(start = start, end_destination = end, mode = mode, google_api_key = api_key)

data_full = route_info.text()

for text in data_full:

    print(text)

