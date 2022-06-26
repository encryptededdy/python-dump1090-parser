import requests
import json

# Filtering out the ones around YSSY
filtered_idents = ["SSM", "CAR"]

# **kwargs is just there to suck up ignored arguments
class Aircraft():
    def __init__(self, hex, seen, rssi, squawk = None, type = None, flight = None, alt_baro = None, alt_geom = None, gs = None, track = None, category = None, lat = None, lon = None, **kwargs):
        self.hex = hex
        self.type = type
        self.ident = flight
        self.alt_baro = alt_baro
        self.gs = gs
        self.track = track
        self.category = category
        self.lat = lat
        self.lon = lon
        self.seen = seen
        self.rssi = rssi
        self.extra_args = kwargs

# URL is probably ip:8080/data/aircraft.json
def parse_aircraft(url):
    request = requests.get(url, timeout=5)
    request_dict = json.loads(request.content)
    request_aircraft = [Aircraft(**ac) for ac in request_dict["aircraft"]]
    return request_aircraft

def in_sky(aircraft):
    return list(filter(lambda ac: ac.alt_baro != "ground" and ac.alt_baro != None, aircraft))

def with_ident(aircraft, filtered = False):
    if filtered:
        return list(filter(lambda ac: ac.ident and ac.ident.strip() and not any(x in ac.ident for x in filtered_idents), aircraft))
    else:
        return list(filter(lambda ac: ac.ident and ac.ident.strip(), aircraft))

def in_sky_and_ident(aircraft):
    return list(filter(lambda ac: ac.ident and ac.ident.strip() and ac.alt_baro != "ground" and ac.alt_baro != None, aircraft))