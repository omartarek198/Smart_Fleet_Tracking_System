import requests

def calculate_route_distance(origin, destination, api_key):
    #recieves 1 comma seperated string consisting of lat,long for origin and another one for destination + the api key
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": origin,
        "destination": destination,
        "key": api_key
    }

    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code == 200 and data["status"] == "OK":
        route = data["routes"][0]
        distance = route["legs"][0]["distance"]["text"]
        return distance
    else:
        return None
api_key = "AIzaSyDzF6-vm0EcngSu-_zPXbKUT0MDgsgM-Jw"

origin = "40.7128,-74.0060"  
destination = "34.0522,-118.2437"

distance = calculate_route_distance(origin, destination, api_key)

if distance:
    print("Route distance:", distance)
else:
    print("unable to calculate ditance")
