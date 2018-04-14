from flask import Flask, render_template, request, redirect, url_for
from geopy.geocoders import Nominatim
from .airnow_worker import AirNowWorker, group_monitor_data, get_nearest_monitor_by_category
from .util import get_bbox

app = Flask(__name__)

KEY = "AIzaSyAkffk3dpehjS06Gg2Vj9hfHeIqF5QZmn4"

worker = AirNowWorker()
geolocator = Nominatim(timeout=5)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/results')
def results():
    lat = float(request.args.get('lat'))
    long = float(request.args.get('long'))
    monitors = worker.get_monitors(get_bbox(lat, long))
    grouped_monitors = group_monitor_data(monitors)
    nearest_monitors = get_nearest_monitor_by_category(lat, long, grouped_monitors)
    return render_template("results.html", lat=lat, long=long, KEY=KEY, monitors=grouped_monitors, nearest_monitors=nearest_monitors)

@app.route('/place_results')
def place_results():
    place_name = request.args.get('place')
    location = geolocator.geocode(place_name)
    return redirect(url_for('results', lat=location.latitude, long=location.longitude))
