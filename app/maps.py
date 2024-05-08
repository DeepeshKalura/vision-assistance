import os
import googlemaps
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()


key = os.getenv("GOOGLEMAPS_API_KEY")
gmaps = googlemaps.Client(key=key)

# Geocoding an address
geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

# Look up an address with reverse geocoding
reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

# Request directions via public transit
now = datetime.now()
directions_result = gmaps.directions("Sydney Town Hall",
                                     "Parramatta, NSW",
                                     mode="transit",
                                     departure_time=now)

# Validate an address with address validation
addressvalidation_result =  gmaps.addressvalidation(['1600 Amphitheatre Pk'], 
                                                    regionCode='US',
                                                    locality='Mountain View', 
                                                    enableUspsCass=True)
# print(addressvalidation_result)
print(directions_result)
# print(reverse_geocode_result)
# print(geocode_result)