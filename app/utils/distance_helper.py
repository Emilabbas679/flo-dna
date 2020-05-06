import googlemaps
from datetime import datetime

API_KEY = 'AIzaSyD6q83jcEbxloW8tYOXLgagBGJ1xrDowHc'
gmaps = googlemaps.Client(API_KEY)


def calculate_distance(pickup, drop):
    now = datetime.now()
    distance = gmaps.directions(
        pickup,
        drop,
        mode='driving',
        avoid='ferries',
        departure_time=now
    )

    return distance[0]['legs'][0]['distance']['value']


def distance_json(pickup, drop):
    now = datetime.now()
    distance = gmaps.directions(
        pickup,
        drop,
        mode='driving',
        avoid='ferries',
        departure_time=now
    )

    return distance


def coordinate_merger(lng, ltd):
    return lng + ',' + ltd


def calculate_price(distance):
    return distance





