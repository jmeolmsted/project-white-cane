
global STOP
from multiprocessing import *
import socket
import signal
from flask_jsonpify import jsonify
from json import dumps
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
from flask import Flask, request, url_for, current_app
from os.path import isfile, join
from os import getpid, getcwd, listdir, kill, system
import webbrowser
import time
from grovepi import *
from picamera import PiCamera


try:
    import simplejson as json
except:
    import json


camera = PiCamera()

# Pin Numbers
vibrator = 3
touch = 2
usft = 6
usfb = 5
usr = 8
usl = 7

pinMode(vibrator, "OUTPUT")
pinMode(touch, "INPUT")

def signal_handler(sig, frame):
    global STOP

    if STOP:
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        kill(getpid(), signal.SIGTERM)
    STOP = True


signal.signal(signal.SIGINT, signal_handler)

ip = ''
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8",80))
ip = s.getsockname()[0]
s.close()

# data = {'ip': ip}

# f = open("./src/assets/ip.json", "w")
# f.write(json.dumps(data))
# f.close()

ipApp = Flask("ipAddress")
ipApi = Api(ipApp)

CORS(ipApp)


class ipAddress(Resource):
    def get(self):
        return jsonify({'ip': ip})


ipApi.add_resource(ipAddress, '/ipAddress')  # Route_1

data = {'entries':  []}

def makeEntry(k, v):
    return {'id': k, 'name': v}

def makeData(usrfb,usrft,usrl,usrr,ir,touch,heart):
    value = {'entry':[{'USRFB': usrfb}, {'USRFT': usrft}, {'USRL': usrl}, {'USRR': usrr}, {'IR': ir}, {'touch': touch}, {'heart': heart}]}
    return value


def getImages():
    directory = getcwd()

    onlyfiles = [f for f in listdir(directory+'/src/assets/images') if isfile(
        join(directory+'/src/assets/images', f))]

    count = 0
    out = {'files': []}

    for x in onlyfiles:
        key = count
        value = x
        out["files"].append(makeEntry(key, value))
        count += 1
    return out

app = Flask(__name__)
api = Api(app)

CORS(app)


@app.route("/")
def hello():
    return jsonify({'text': 'Hello World!'})


class Files(Resource):
    def get(self):
        return getImages()

class Data(Resource):
    def get(self):
        valUSRFB = converter(ultrasonicRead(usfb))
        valUSRFT = converter(ultrasonicRead(usft))
        valUSRL = converter(ultrasonicRead(usl))
        valUSRR = converter(ultrasonicRead(usr))
        valTouch = digitalRead(touch)
        data["entries"] = makeData(valUSRFB,valUSRFT,valUSRL,valUSRR,valIR,valTouch,valHeart)
        return jsonify(data)

api.add_resource(Files, '/files')  # Route_1
api.add_resource(Data, '/data')

def converter(cm):
    feet = (cm * 0.393701)/12
    return feet

def runIp():
    ipApp.run(port=5002)

def runFile():
    app.run(host=ip)

def runIonic():
    system('ionic serve --external --no-open')
    
def openWeb():
    url = 'http://' + ip + ':8100'
    webbrowser.open(url)

def main():
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    pool = Pool(processes=2)
    try:
        ipSite = pool.apply_async(runIp)
        fileSite = pool.apply_async(runFile)
        #ionic = pool.apply_async(runIonic)
        #browser = pool.apply_async(openWeb)
        
        pool.close()
        pool.join()
    except:
        pool.terminate()

if __name__ == '__main__':
    main()
