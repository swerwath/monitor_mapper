import os
import sys
import json
import datetime
import urllib.request
from rtree import index
from .util import get_distance

API_BASE_URL = "https://airnowapi.org/aq/data/"
PARAMS = "O3,PM25,NO2,SO2"
RETURN_TYPE = "a"
RETURN_FORMAT = "application/json"
API_KEY = os.environ['AIRNOW_KEY']
CA_BOUNDING_BOX = "-124.644883,31.779242,-114.445046,41.998718"

REQUEST_URL = API_BASE_URL \
      + "?parameters=" + PARAMS \
      + "&bbox=" + CA_BOUNDING_BOX \
      + "&datatype=" + RETURN_TYPE \
      + "&format=" + RETURN_FORMAT \
      + "&api_key=" + API_KEY

def fetch_ca_air_data():
    with urllib.request.urlopen(REQUEST_URL) as response:
        resp = response.read()
    return resp

def group_monitor_data(monitors):
    to_ret = {m.param : [] for m in monitors}
    for m in monitors:
        to_ret[m.param].append(m.to_json_dict())
    return to_ret

# Takes monitor json dicts, returns monitor json dicts
def get_nearest_monitor(lat, long, monitors):
    sorted_monitors = sorted(monitors, key=lambda mon : get_distance(lat, long, mon['latitude'], mon['longitude']))
    return sorted_monitors[0]

# Map of "SO2" -> [monitor_json_doct, dist]
def get_nearest_monitor_by_category(lat, long, grouped_monitors):
    to_ret = {}
    for category in grouped_monitors:
        nearest_monitor = get_nearest_monitor(lat, long, grouped_monitors[category])
        dist = get_distance(lat, long, nearest_monitor['latitude'], nearest_monitor['longitude'])
        to_ret[category] = [nearest_monitor, dist]
    return to_ret


class MonitorData():
    def __init__(self, api_resp_obj):
        self.latitude = api_resp_obj['Latitude']
        self.longitude = api_resp_obj['Longitude']
        self.param = api_resp_obj['Parameter']
        self.unit = api_resp_obj['Unit']
        self.aqi = api_resp_obj['AQI']

    def to_json_dict(self):
        return {'AQI' : self.aqi, 'latitude' : self.latitude, 'longitude' : self.longitude, 'param' : self.param}

class AirNowWorker():
    def __init__(self, refresh_minutes=60):
        self.refresh_minutes = refresh_minutes
        self.refresh()

    def refresh(self):
        api_response = fetch_ca_air_data()
        monitor_list = json.loads(api_response)
        data_objs = [MonitorData(m) for m in monitor_list]

        idx = index.Index()
        id_map = {}
        for i, do in enumerate(data_objs):
            coords = (do.latitude, do.longitude, do.latitude, do.longitude)
            idx.insert(i, coords)
            id_map[i] = do
        self.id_map = id_map
        self.idx = idx

        self.last_refresh = datetime.datetime.now()

    def get_monitors(self, bbox):
        now = datetime.datetime.now()
        mins_since_refresh = (now - self.last_refresh).total_seconds() / 60.0
        if mins_since_refresh > 60:
            try:
                self.refresh()
            except Exception as e:
                print("Failed to refresh AirNow data: " + str(e))

        monitor_ids = self.idx.intersection(bbox)
        monitors_objs = [self.id_map[mid] for mid in monitor_ids]

        return monitors_objs
