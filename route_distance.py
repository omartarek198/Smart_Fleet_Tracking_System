import requests

def calculate_route_distance(origin, destination):
    api_key = "AIzaSyDzF6-vm0EcngSu-_zPXbKUT0MDgsgM-Jw"
    #input : 2 strings represnting the origin and destination cordinates in the form of 
    # origin ="longitude,latidue" , source = "longitude,latidue"
    #output : None if failed to get response else, returns route distance and eta
    
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
        duration = route["legs"][0]["duration"]["text"]
        return distance,duration
    else:
        return None


origin = "40.7128,-74.0060"  
destination = "34.0522,-118.2437"

distance = calculate_route_distance(origin, destination)

if distance:
    print("Route distance:", distance)
else:
    print("unable to calculate ditance")
