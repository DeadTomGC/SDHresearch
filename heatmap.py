import pandas as pd
from geopy.geocoders import Nominatim
import folium
from folium.plugins import HeatMap
import time
import openpyxl


import requests

def geolocate_address(address, api_key):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json?"
    params = {
        'address': address,
        'key': api_key
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'OK':
            # Extract latitude and longitude
            latitude = data['results'][0]['geometry']['location']['lat']
            longitude = data['results'][0]['geometry']['location']['lng']
            return latitude, longitude
        else:
            return None, None
    else:
        print(f"HTTP error {response.status_code}")
        return None, None



# Load the addresses from a csv file
df = pd.read_excel('data.xlsx', engine="openpyxl")
#geolocator = Nominatim(user_agent="Heritage_Valley_Research")
api_key = open('API_token.txt').readline()


# Create an empty list to hold the geocoded coordinates
location_list = []
not_found_list = []

for index, row in df.iterrows():
    try:
        address = row['Address']
        if isinstance(address, str):
            latitude, longitude = geolocate_address(address, api_key)
        
            if latitude is not None and longitude is not None:
                location_list.append([latitude, longitude])
                print("Located: " + address + " at " + str(latitude) + " , " + str(longitude))
            else:
                print("Failed to locate: " + address)
                not_found_list.append(address)
            time.sleep(0.1)
    except Exception as e:
        print(f"Error with row {index}: {e}")
        not_found_list.append("Error with row {index}: {e}")
        
    

file = open("found_locations.txt",'w')
file.write(str(location_list))
file.close()
file = open("not_found_locations.txt",'w')
file.write(str(not_found_list))
file.close()

print(location_list)

# Create a base map
m = folium.Map(location=[0, 0], zoom_start=2)

# Add a heatmap to the base map
HeatMap(location_list).add_to(m)

# Save the map to a file
m.save("density_map.html")
