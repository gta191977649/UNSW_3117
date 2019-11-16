from flask import Flask
from flask import jsonify
from flask import Response
from flask_cors import CORS
import json
import random
app = Flask(__name__)
CORS(app)

time_slice_len = 60
current_step = 0
freq_data = {}
freq_data["x"] = []
freq_data["y"] = []

shimmer_data = {}
shimmer_data["x"] = []
shimmer_data["y"] = []

def generateRandom():
    #Random generate states
    statechouse = random.randint(0,4)
    rand_state = None
    if(statechouse == 0):
        rand_state = {'weak':random.randint(0,5)}
    elif(statechouse == 1):
        rand_state = {'mid_weak': random.randint(0, 5)}
    elif(statechouse == 2):
        rand_state = {'mid': random.randint(0, 5)}
    elif(statechouse == 3):
        rand_state =  {'mid_strong': random.randint(0, 5)}
    elif(statechouse == 4):
        rand_state = {'strong': random.randint(0, 5)}
    #Random generate charts data
    #Generate Frequqnce Data in intervals
    global current_step
    current_step += 1
    if(len(freq_data["x"]) > time_slice_len):
        freq_data["x"].pop(0)
        freq_data["y"].pop(0)

    freq_data["x"].append(current_step)
    freq_data["y"].append(random.randint(0, 5))

    if(len(shimmer_data["x"]) > time_slice_len):
        shimmer_data["x"].pop(0)
        shimmer_data["y"].pop(0)

    shimmer_data["x"].append(current_step)
    shimmer_data["y"].append(random.randint(8, 10))


    data = {
        "state": rand_state,
        "freq":freq_data,
        "shimmer":shimmer_data,
    }
    return data
@app.route("/")
def hello():
    data = generateRandom()
    print(data)

    data = json.dumps(data)
    resp = Response(data, status=200, mimetype='application/json')
    return resp

if __name__ == "__main__":
    app.run()