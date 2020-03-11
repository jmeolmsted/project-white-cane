from picamera import PiCamera
from grovepi import *
from flask_restful import Api, Resource
from flask_jsonpify import jsonify
from flask_cors import CORS, cross_origin
from flask import Flask, current_app, request, url_for
from os.path import isfile, join
from os import getcwd, getpid, kill, listdir, system
from multiprocessing import *
from json import dumps
from pulsesensor import Pulsesensor
import webbrowser
import time
import socket
import signal
import qwiic_vl53l1x
global STOP


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

# def signal_handler(sig, frame):
#     global STOP

#     if STOP:
#         signal.signal(signal.SIGINT, signal.SIG_IGN)
#         kill(getpid(), signal.SIGTERM)
#     STOP = True


# signal.signal(signal.SIGINT, signal_handler)

ip = ''
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = s.getsockname()[0]
s.close()

# ipApp = Flask("ipAddress")
# ipApi = Api(ipApp)

# CORS(ipApp)


# class ipAddress(Resource):
#     def get(self):
#         return jsonify({'ip': ip})


# ipApi.add_resource(ipAddress, '/ipAddress')  # Route_1

data = {'entries':  []}


def makeEntry(k, v):
    return {'id': k, 'name': v}


def makeData(usrfb, usrft, usrl, usrr, ir, touch, heart):
    value = {'entry': [{'USRFB': usrfb}, {'USRFT': usrft}, {'USRL': usrl}, {
        'USRR': usrr}, {'IR': ir}, {'touch': touch}, {'heart': heart}]}
    return value


def getData():
    valUSRFB = round(converter(ultrasonicRead(usfb)), 1)
    valUSRFT = round(converter(ultrasonicRead(usft)), 1)
    valUSRL = round(converter(ultrasonicRead(usl)), 1)
    valUSRR = round(converter(ultrasonicRead(usr)), 1)
    valIR = round(irConverter(irDist()), 1)
    valTouch = True if digitalRead(touch) == 1 else False
    valHeart = getHeart()
    data["entries"] = makeData(
        valUSRFB, valUSRFT, valUSRL, valUSRR, valIR, valTouch, valHeart)
    return data


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
        return getData()


api.add_resource(Files, '/files')  # Route_1
api.add_resource(Data, '/data')




def irDist():
    mySensor = qwiic_vl53l1x.QwiicVL53L1X()

#	if mySensor.isConnected() == False:
#		print("The Laser is not connected.")
#		return

    mySensor.sensor_init()
    mySensor.start_ranging()
    time.sleep(0.005)
    distance = mySensor.get_distance()
    time.sleep(00.005)
    mySensor.stop_ranging()

    # print("Distance (mm): %s " % distance)
    return distance


def getHeart():
    p = Pulsesensor()
    p.startAsyncBPM()
    bpm = p.BPM
    return bpm
    p.stopAsyncBPM

def irConverter(mm):
    cm = mm/10
    return (converter(cm))


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
    #  main()
    runFile()
