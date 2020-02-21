global STOP
from multiprocessing import *
import socket
import signal
from flask_jsonpify import jsonify
from json import dumps
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
from flask import Flask, request, url_for, current_app
import sys
from os.path import isfile, join
from os import *
import urllib.request
import webbrowser


try:
    import simplejson as json
except:
    import json


def signal_handler(sig, frame):
    global STOP

    if STOP:
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        kill(getpid(), signal.SIGTERM)
    STOP = True


signal.signal(signal.SIGINT, signal_handler)

ip = socket.gethostbyname(socket.gethostname())

ipApp = Flask("ipAddress")
ipApi = Api(ipApp)

CORS(ipApp)

@ipApp.route("/")
def hello():
    return jsonify({'text': 'Hello World!'})


class ipAddress(Resource):
    def get(self):
        return jsonify({'ip': ip})


ipApi.add_resource(ipAddress, '/ipAddress')  # Route_1

directory = getcwd()

onlyfiles = [f for f in listdir(directory+'/src/assets/images') if isfile(
    join(directory+'/src/assets/images', f))]

count = 0
out = {'files': []}


def makeEntry(k, v):
    return {'id': k, 'name': v}


for x in onlyfiles:
    key = count
    value = x
    out["files"].append(makeEntry(key, value))
    count += 1

app = Flask(__name__)
api = Api(app)

CORS(app)


@app.route("/")
def hello():
    return jsonify({'text': 'Hello World!'})


class Files(Resource):
    def get(self):
        return out


api.add_resource(Files, '/files')  # Route_1

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
