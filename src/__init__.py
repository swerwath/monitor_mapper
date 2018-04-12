from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/results')
def results():
    lat = request.args.get('lat')
    long = request.args.get('long')
    return render_template("results.html", lat=lat, long=long)
