import time
import numpy as np
import math
import json
import base64
from google.cloud import pubsub_v1
from google.cloud import iot_v1
from googleapiclient import discovery
from google.oauth2 import service_account
import threading
from test import *
# WEB代码 ###################
from flask import Flask
from flask import jsonify
from flask import Response
from flask_cors import CORS
# WEB代码 ###################

webservice = Flask(__name__)
CORS(webservice)
#数据(目前数据)
state = [0,0,0,0,0]
time_slice_len = 60 #时间总切片长度（秒）
current_step = 0 #目前的Step（会每秒逐步递增）
freq_data = {} #频率数据
freq_data["x"] = [] #频率数据x
freq_data["y"] = [] #频率数据y

shimmer_data = {} #Shimmer 数据
shimmer_data["x"] = [] #Shimmer 数据x
shimmer_data["y"] = [] #Shimmer 数据y
vol_data = {} #vol 数据
vol_data["x"] = [] #Shimmer 数据x
vol_data["y"] = [] #Shimmer 数据y
#判断是不是apnea
apnea = False

#打包准备前端web数据
def packData(inState,freq,shimmer,vol):
    global state
    for i in range(0, len(state)):
        state[i] += inState[i]

    global current_step
    current_step += 1
    if (len(freq_data["x"]) > time_slice_len):
        freq_data["x"].pop(0)
        freq_data["y"].pop(0)

    freq_data["x"].append(current_step)
    freq_data["y"].append(freq)

    if (len(shimmer_data["x"]) > time_slice_len):
        shimmer_data["x"].pop(0)
        shimmer_data["y"].pop(0)

    shimmer_data["x"].append(current_step)
    shimmer_data["y"].append(shimmer)


    #shimmer_data["y"].append(breath)

    if (len(vol_data["x"]) > time_slice_len):
        vol_data["x"].pop(0)
        vol_data["y"].pop(0)
    vol_data["x"].append(current_step)
    breath = 45 - float(vol)
    vol_data["y"].append(breath)
@webservice.route("/")
def services():
    data = {
        "state": state,
        "freq": freq_data,
        "shimmer": shimmer_data,
        "vol": vol_data,
        "apnea": apnea,
    }

    #print(data)
    data = json.dumps(data)
    resp = Response(data, status=200, mimetype='application/json')
    return resp

def runWebServices():
    webservice.run(host='0.0.0.0')


credentials = service_account.Credentials.from_service_account_file("./31170-f5cbdfce39ba.json")
service_account_json = "./31170-f5cbdfce39ba.json"
cloud_region = "us-central1"
registry_id = "my-iot-registry"
device_id = "d0123EF5E2C2C9AD9FE"
#credentials = service_account.Credentials.from_service_account_file("./n3117-257504-2b339a673323.json")
#credentials = service_account.Credentials.from_service_account_file("./supple-rex-257523-cf39afcb79e8.json")

#GOOGLE_APPLICATION_CREDENTIALS = "C:/Users/Yitian Chen.DESKTOP-TIIP443/Desktop/unsw/3117/signal_processing/31170-f5cbdfce39ba.json"
GOOGLE_APPLICATION_CREDENTIALS = "C:/Users/Yitian Chen.DESKTOP-TIIP443/Desktop/unsw/3117/signal_processing/n3117-257504-2b339a673323.json"

project_id = "balmy-visitor-255612"
#topic_name = 
#project_id = "supple-rex-257523"
#project_id = "n3117-257504"
subscription_name = "monitor-sub"
subscriber = pubsub_v1.SubscriberClient(credentials = credentials)
publisher = pubsub_v1.PublisherClient(credentials = credentials)
#topic_name = publisher.topic_path(project_id,)
topic_name = "projects/balmy-visitor-255612/topics/events"
topic_path = publisher.topic_path(project_id,topic_name)
#subscriber = pubsub_v1.SubscriberClient()
N_size = 200
vol = [0]
process_arr = np.zeros(N_size)

for i in range(N_size):
    process_arr[i] = -1

    
# The `subscription_path` method creates a fully qualified identifier

# in the form `projects/{project_id}/subscriptions/{subscription_name}`

subscription_path = subscriber.subscription_path(project_id, subscription_name)
def get_client(service_account_json):
    """Returns an authorized API client by discovering the IoT API and creating
    a service object using the service account credentials JSON."""
    api_scopes = ['https://www.googleapis.com/auth/cloud-platform']
    api_version = 'v1'
    discovery_api = 'https://cloudiot.googleapis.com/$discovery/rest'
    service_name = 'cloudiotcore'

    credentials = service_account.Credentials.from_service_account_file(
            service_account_json)
    scoped_credentials = credentials.with_scopes(api_scopes)

    discovery_url = '{}?version={}'.format(
            discovery_api, api_version)

    return discovery.build(
            service_name,
            api_version,
            discoveryServiceUrl=discovery_url,
            credentials=scoped_credentials)

def send_command(
        service_account_json, project_id, cloud_region, registry_id, device_id,
        command):
    """Send a command to a device."""
    # [START iot_send_command]
    print('Sending command to device')
    client = iot_v1.DeviceManagerClient(credentials = credentials)
    device_path = client.device_path(
        project_id, cloud_region, registry_id, device_id)

    data = command.encode('utf-8')

    return client.send_command_to_device(device_path, data)

def callback(message):
    msg = message.data
    data = json.loads(msg.decode("utf-8"))
    print(data["pump"])
    vol[0] = data["pump"]
    message.ack()

def publish(client, topic_path):
    messages = ['0']
    #for line in data_lines:
    line = 1
    messages.append({'data': line})
    body = {'messages': messages}
    str_body = json.dumps(body)
    data = base64.urlsafe_b64encode(bytearray(str_body, 'utf8'))
    client.publish(topic_path, data=data)

subscriber.subscribe(subscription_path, callback=callback)

# The subscriber is non-blocking. We must keep the main thread from
# exiting to allow it to process messages asynchronously in the background.

print('Listening for messages on {}'.format(subscription_path))
client = get_client(service_account_json)
timeout = 0
#send_command(service_account_json, project_id, cloud_region, registry_id, device_id,"1")
states = [0,0,0,0,0]
len_states = 5
last_state = [0]
def update_states(state):
    for i in range(len_states-1):
        states[i] = states[i+1]
    states[len_states - 1] = state

def mean_states():
    avgs = 0
    for i in range(len_states):
        avgs = avgs + states[i]
    return avgs

def thread_function():
    #try:
    update_sig(float(vol[0]))
    avgs = mean_states()
    [shim,freq,five_state,steep] = is_sleep_apnea()

    #保存&更新接收到的数据到WEB服务
    packData(five_state,freq,shim,float(vol[0]))

    if((shim < 1.6 and steep < 2) or (shim < 2.5 and steep < 0.5)):
        if((shim < 1.6 and steep < 2)):
            print("sta1", shim, steep)
        if((shim < 2.5 and steep < 0.5)):
            print("sta1")
        state = 1
    else:
        state = 0
    update_states(state)
    if(state == 1 and avgs >= 3 and (float(vol[0]) > 39)):
        send_command(service_account_json, project_id, cloud_region, registry_id, device_id,"0")
        apnea = True
        print("apnea")
    #if((last_state[0] == 1 and state == 0) and (float(vol[0]) < 39)):
    if((state == 0) and (float(vol[0]) < 39)):
        send_command(service_account_json, project_id, cloud_region, registry_id, device_id,"1")
        apnea = False
        print("no apnea")
    last_state[0] = state
    #except:
        #print("not connected!")


try:
    send_command(service_account_json, project_id, cloud_region, registry_id, device_id,"1")
except:
    time.sleep(1)
tWebService = threading.Thread(target = runWebServices, args = ())
tWebService.start()

def main2():
    while True:
        time.sleep(1)
        tRecieve = threading.Thread(target = thread_function, args = ())
        tRecieve.start()

t_new = threading.Thread(target = main2, args = ())
t_new.start()







