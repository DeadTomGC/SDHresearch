import pandas as pd
import time
import openpyxl
import sys
import yaml

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
    
api_key = open('API_token.txt').readline()
map_id = open('map_id.txt').readline()
# Create an empty list to hold the geocoded coordinates
found_home_list = []
not_found_home_list = []
found_grocery_list = []
not_found_grocery_list = []
heat_list = []
grocery_marker_list = []

if len(sys.argv)>1 and sys.argv[1].endswith('.yml'):
    with open(sys.argv[1],'r') as locations_file:
        dataDict = yaml.safe_load(locations_file)
    
    found_home_list = dataDict["foundHomes"]
    not_found_home_list = dataDict["notFoundHomes"]
    found_grocery_list = dataDict["foundGroceries"]
    not_found_grocery_list = dataDict["notFoundGroceries"]

    for location in found_home_list:
        latitude = location[0]
        longitude = location[1]
        heat_list.append(f'new google.maps.LatLng({str(latitude)},{str(longitude)})')
        
    for location in found_grocery_list:
        latitude = location[0]
        longitude = location[1]
        grocery_marker_list.append(f'new google.maps.marker.AdvancedMarkerElement({{map,zIndex:1,collisionBehavior: google.maps.CollisionBehavior.REQUIRED,position: {{ lat: {latitude}, lng: {longitude} }},content: parser.parseFromString(cartSvgString, "image/svg+xml").documentElement,}}),')
else:
    # Load the addresses from an xlsx file
    if len(sys.argv)>1 and sys.argv[1].endswith('.xlsx'):
        df = pd.read_excel(sys.argv[1], engine="openpyxl")
    else:
        df = pd.read_excel('data.xlsx', engine="openpyxl")





    for index, row in df.iterrows():
        try:
            address = row['Address']
            groceryAddr = row['Groceries']
            if isinstance(address, str):
                latitude, longitude = geolocate_address(address, api_key)
            
                if latitude is not None and longitude is not None:
                    found_home_list.append([latitude, longitude])
                    print("Located: " + address + " at " + str(latitude) + " , " + str(longitude))
                    heat_list.append(f'new google.maps.LatLng({str(latitude)},{str(longitude)})')
                else:
                    print("Failed to locate: " + address)
                    not_found_home_list.append(address)
            if isinstance(groceryAddr,str):
                latitude, longitude = geolocate_address(groceryAddr, api_key)
                if latitude is not None and longitude is not None:
                    found_grocery_list.append([latitude, longitude])
                    print("Located grocery: " + address + " at " + str(latitude) + " , " + str(longitude))
                    grocery_marker_list.append(f'new google.maps.marker.AdvancedMarkerElement({{map,zIndex:1,collisionBehavior: google.maps.CollisionBehavior.REQUIRED,position: {{ lat: {latitude}, lng: {longitude} }},content: parser.parseFromString(cartSvgString, "image/svg+xml").documentElement,}}),')
                else:
                    print("Failed to locate: " + groceryAddr)
                    not_found_grocery_list.append(groceryAddr)
                
        except Exception as e:
            print(f"Error with row {index}: {e}")
            not_found_home_list.append("Error with row {index}: {e}")
            
dataDict = {"foundHomes":found_home_list,
            "foundGroceries":found_grocery_list,
            "notFoundHomes":not_found_home_list,
            "notFoundGroceries":not_found_grocery_list}

file = open("locationData.yml",'w')
file.write(yaml.dump(dataDict))
file.close()


map_html = open('map_start.html','r').read()

map_html = map_html.replace('origin_coordinates',f'{found_home_list[0][0]},{found_home_list[0][1]}')

heat_element_str = ''

for heat_element in heat_list:
    heat_element_str += '          ' + heat_element + ',\r\n'

groceries_str = ''

for grocery in grocery_marker_list:
    groceries_str += '          ' + grocery + '\r\n'

map_html = map_html.replace('heat_list',heat_element_str[:-3])
map_html = map_html.replace('insert_key',api_key)
map_html = map_html.replace('grocery_list',groceries_str[:-3])
map_html = map_html.replace('map_id',map_id)

file = open("marker_map.html",'w')
file.write(map_html)
file.close()


