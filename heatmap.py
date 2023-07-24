import pandas as pd
from geopy.geocoders import Nominatim
import folium
from folium.plugins import HeatMap
import time

# Load the addresses from a csv file
df = pd.read_csv('data.csv')

geolocator = Nominatim(user_agent="Heritage_Valley_Research")

# Create an empty list to hold the geocoded coordinates
location_list = []

for index, row in df.iterrows():
    try:
        address = row['Address']
        location = geolocator.geocode(address)
        
        if location:
            location_list.append([location.latitude, location.longitude])
        else:
            print("Failed to locate: " + address)
    except Exception as e:
        print(f"Error with row {index}: {e}")
        
    time.sleep(1)

file = open("found_locations.txt",'w')
file.write(str(location_list))
file.close()

print(location_list)

# Create a base map
m = folium.Map(location=[0, 0], zoom_start=2)

# Add a heatmap to the base map
HeatMap(location_list).add_to(m)

# Save the map to a file
m.save("density_map.html")
