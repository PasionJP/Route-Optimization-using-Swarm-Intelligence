# import module
from geopy.geocoders import Nominatim

# initialize Nominatim API
geolocator = Nominatim(user_agent="geoapiExercises")

# Latitude & Longitude input
Latitude = "14.656891520422409"
Longitude = "121.03045870106894"
# 14.658896897859847, 121.03038696254546
# 14.652889668911557, 121.04933098437206
 
location = geolocator.reverse(Latitude+","+Longitude)
address = location.raw['address']
addr1 = address[list(address.keys())[0]]
print(address)
# locAddress = address.get('road', '') + " " + address.get('quarter', '') + " " + address.get('city', '') + " " + address.get('region', '')
 