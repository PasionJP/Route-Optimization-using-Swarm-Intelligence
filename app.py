from flask import Flask, render_template, request, redirect, url_for
import threading
import Map.ACOvPSO
import json
import os

app = Flask(__name__, template_folder='template')
addresses = []
optimizationResults = []
distance_or_time = ""
psoTime = ""
acoTime = ""

@app.route('/', methods=['GET', 'POST'])
def index():   
    return render_template('index.html')

@app.route('/loading', methods=['GET', 'POST'])
def loading():
    return render_template("loading.html")

@app.route('/results', methods=['GET', 'POST'])
def results():
    global optimizationResults
    global time
    template_folder = app.template_folder
    file_path_aco = os.path.join(template_folder, 'ACOmap.html')
    file_path_pso = os.path.join(template_folder, 'PSOmap.html')

    if os.path.exists(file_path_aco):
        os.remove(file_path_aco)
    if os.path.exists(file_path_pso):
        os.remove(file_path_pso)

    optimizationResults, time = Map.ACOvPSO.ACOvPSO.generateCalculatedMap(addresses, distance_or_time, algo)
    return "Map creation done."

@app.route('/address', methods=['GET', 'POST'])
def address():
    global addresses
    global distance_or_time
    global algo
    if request.method == 'POST':
        addresses = request.json['items']
        distance_or_time =  request.json['radioValue1']
        distance_or_time = int(distance_or_time)
        algo =  request.json['radioValue2']
        algo = int(algo)
    return "Address retrieval done."

@app.route('/test')
def test():    
    print("TEST")
    return render_template('ACOmap.html')

@app.route('/ACOmap.html')
def ACOmap():    
    return render_template('ACOmap.html')

@app.route('/PSOmap.html')
def PSOmap():    
    return render_template('PSOmap.html')

@app.route('/submit', methods=["GET"])
def submit():
    print("ADDRESSES", addresses)
    print("OPTIMIZED:", optimizationResults)
    # routeArrangement = [addresses[optimizationResults[0][1][i]] for i, address in enumerate(addresses)]
    if algo == 0:
        if distance_or_time == 0:
            acoRouteArrangement = ' → '.join(optimizationResults[1])
            acoResultMessage = "The best route is " + str(acoRouteArrangement) + " with " + str(round(optimizationResults[0][1],1)) + "mins total travel time."
        else:
            acoRouteArrangement = ' → '.join(optimizationResults[1])
            acoResultMessage = "The best route is " + str(acoRouteArrangement) + " with " + str(round(optimizationResults[0][1],1)) + "km total travel distance."
        return render_template('two-column.html', map='ACOmap', result=acoResultMessage, time=time, algoUsed="Ant Colony Optimization")
    else:
        if distance_or_time == 0:
            psoRouteArrangement = ' → '.join(optimizationResults[1])
            psoResultMessage = "The best route is " + str(psoRouteArrangement) + " with " + str(round(optimizationResults[0][1],1)) + "mins total travel time."
        else:
            psoRouteArrangement = ' → '.join(optimizationResults[1])
            psoResultMessage = "The best route is " + str(psoRouteArrangement) + " with " + str(round(optimizationResults[0][1],1)) + "km total travel distance."
        return render_template('two-column.html', map='PSOmap', result=psoResultMessage, time=time, algoUsed="Particle Swarm Optimization")

if __name__ == '__main__':
    app.run()