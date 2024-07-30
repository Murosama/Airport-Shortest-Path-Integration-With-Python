from flask import Flask, request, render_template
import numpy as np
from scipy.spatial.distance import euclidian
import networkx as nx

app = Flask(__name__)

def calculate_distance(locations,plane_location):
    distances = {}
    for place, coords in location.items():
        distances[place] = euclidian(cords, plane_location)
    return distances

def create_graph(locations, plane_location):
    G = nx.Graph()
    for place, coords in locations.items():
        G.add_edge("plane", place, weight=euclidian(coords, plane_location))
        for other_place, other_coords in locations.items():
            if place != other_place:
                G.add_edge(place, other_place, weight=euclidian(coords, other_coords))
    return G

def optimize_routes(G):
    return nx.shortest_path(G, source="plane", weight="weight")

def assign_trips(routes, car_capacity, total_cargo, num_cars):
    trips = []
    remaining_cargo = total_cargo
    while remaining_cargo > 0:
        for car in range(num_cars):
            if remaining_cargo <=0:
                break
            trip_cargo = min(car_capacity, remaining_cargo)
            trips.append({"car": car, "cargo_amount": trip_cargo, "route": routes})
            remaining_cargo -= trip_cargo
        return trips
    
def calculate_load_time(cargo_amount, car_capacity):
    return sum(G.edges[edge]["weight"] for edge in zip(route[:-1], route[1:]))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/optimize', methods=['POST'])

def optimize():
    num_places = int(request.form['num_places'])
    car_capacity = int(request.form['car_capacity'])
    num_cars = int(request.form['num_cars'])
    plance_location = tuple(map(float, request.form['plane_location'].split(',')))


    locations = {}
    total_cargo = 0
    for i in range(num_places):
        place = request.form[f'place{i+1}']
        coords = tuple(map(float, request.form[f'coords{i+1}'].split(',')))
        locations[place] = coords
        total_cargo += float(request.form[f'cargo{i+1}'])

    G = create_graph (locations, plane_location)
    routes = optimize_routes(G)
    trips = assign_trips(routes, car_capacity, total_cargo, num_cars)

    total_time = 0
    for trip in trips:
        load_time = calculate_load_time(trip["cargo_amount"], car_capacity)
        travel_time = calculate_travel_time(trip["route"], G)
        total_time += load_time + travel_time

    return render_template('resut.html', total_time=total_time, trips=trips)

if __name__ == '__main__':
    app.run(debug=True)    