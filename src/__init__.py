from flask import Flask, render_template, request
from .airnow_worker import AirNowWorker, group_monitor_data
from .util import get_bbox

app = Flask(__name__)

KEY = "AIzaSyAkffk3dpehjS06Gg2Vj9hfHeIqF5QZmn4"

worker = AirNowWorker()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/results')
def results():
    lat = float(request.args.get('lat'))
    long = float(request.args.get('long'))
    monitors = worker.get_monitors(get_bbox(lat, long))
    grouped_monitors = group_monitor_data(monitors)
    return render_template("results.html", lat=lat, long=long, KEY=KEY, monitors=grouped_monitors)
