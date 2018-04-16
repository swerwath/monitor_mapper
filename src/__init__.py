from flask import Flask, render_template, request, redirect, url_for
from geopy.geocoders import Nominatim
from .airnow_worker import AirNowWorker, group_monitor_data, get_nearest_monitor_by_category
from .util import get_bbox
from .tri_database import TRIDatabase

app = Flask(__name__)

KEY = "AIzaSyAkffk3dpehjS06Gg2Vj9hfHeIqF5QZmn4"

worker = AirNowWorker()
tri = TRIDatabase()
geolocator = Nominatim(timeout=5)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/results')
def results():
    lat = float(request.args.get('lat'))
    long = float(request.args.get('long'))
    bbox = get_bbox(lat, long)

    monitors = worker.get_monitors(bbox)
    grouped_monitors = group_monitor_data(monitors)
    nearest_monitors = get_nearest_monitor_by_category(lat, long, grouped_monitors)

    facilities = tri.get_facilities(bbox)
    facilities_dicts = [f.to_json_dict() for f in facilities]

    return render_template("results.html", lat=lat, long=long, KEY=KEY, monitors=grouped_monitors, nearest_monitors=nearest_monitors, facilities=facilities_dicts)

@app.route('/place_results')
def place_results():
    place_name = request.args.get('place')
    location = geolocator.geocode(place_name)
    return redirect(url_for('results', lat=location.latitude, long=location.longitude))
