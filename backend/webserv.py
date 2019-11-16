from flask import Flask
from flask import jsonify
from flask import Response
from flask_cors import CORS
import json
import random
app = Flask(__name__)
CORS(app)

def generateRandom():
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
    data = {
        "state": rand_state,
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