import json

import requests

class Location:
    def __init__(self, address, location):
        self.formatted_address = address
        self.location = location

apikey = ""

def get_coordinates(query):
    query = query.replace(" ", "+")
    query = query.replace("&", "+")
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=" + query + "&key=" + apikey
    response = requests.get(url=url)
    responseObject = json.loads(response.text)
    if responseObject["status"] == "OK":
        try:
            return Location(address=responseObject["results"][0]["formatted_address"],
                    location=responseObject["results"][0]["geometry"]["location"])
        except:
            print("Unable to get location for: " + query)
            print(responseObject)
            return None
    print(responseObject["status"])
    return None
