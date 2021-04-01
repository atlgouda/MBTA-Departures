import requests
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def home():
    r = requests.get(
        'https://api-v3.mbta.com/routes?sort=type&filter%5Btype%5D=0%2C1')
    routes = r.json()
    return render_template("home.html", routes=routes['data'])


@app.route('/routes/<route_id>')
def selected_route(route_id):
    selected_route_raw = requests.get(
        'https://api-v3.mbta.com/routes/{}'.format(route_id))
    selected_route = selected_route_raw.json()
    s = requests.get(
        'https://api-v3.mbta.com/stops?filter%5Broute%5D={}'.format(route_id))
    stops = s.json()
    return render_template("stops.html", stops=stops['data'], route=selected_route['data'])


@app.route('/routes/<route_id>/stop/<stop_id>')
def selected_stop(stop_id, route_id):
    selected_route_raw = requests.get(
        'https://api-v3.mbta.com/routes/{}'.format(route_id))
    selected_route = selected_route_raw.json()
    return render_template("direction.html", route_id=route_id, stop_id=stop_id, route=selected_route['data'])


@app.route('/routes/<route_id>/stop/<stop_id>/direction/<direction>')
def departure(stop_id, route_id, direction):
    r = requests.get(
        'https://api-v3.mbta.com/predictions?filter%5Bdirection_id%5D={}&filter%5Bstop%5D={}&filter%5Broute%5D={}'.format(direction, stop_id, route_id))
    prediction = r.json()
    selected_route_raw = requests.get(
        'https://api-v3.mbta.com/routes/{}'.format(route_id))
    selected_route = selected_route_raw.json()
    stop_raw = requests.get('https://api-v3.mbta.com/stops/{}'.format(stop_id))
    stop = stop_raw.json()
    return render_template("departure.html", prediction=prediction['data'][0], route=selected_route['data'],
                           direction=int(direction), stop=stop['data'])
