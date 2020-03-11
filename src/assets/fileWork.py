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
from datetime import datetime
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

# Pin Numbers
vibrator = 3
touch = 2
usft = 6
usfb = 5
usr = 8
usl = 7

pinMode(vibrator, "OUTPUT")
pinMode(touch, "INPUT")

ip = ''
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = s.getsockname()[0]
s.close()

def makeEntry(k, v):
    return {'id': k, 'name': v}


def makeData(usrfb, usrft, usrl, usrr, ir, touch, heart):
    value = {'entry': [{'USRFB': usrfb}, {'USRFT': usrft}, {'USRL': usrl}, {
        'USRR': usrr}, {'IR': ir}, {'touch': touch}, {'heart': heart}]}
    return value


def getData():
    data = {'entries':  []}
    valUSRFB = round(converter(ultrasonicRead(usfb)), 1)
    valUSRFT = round(converter(ultrasonicRead(usft)), 1)
    valUSRL = round(converter(ultrasonicRead(usl)), 1)
    valUSRR = round(converter(ultrasonicRead(usr)), 1)
    valIR = round(irConverter(irDist()), 1)
    valTouch = True if digitalRead(touch) == 1 else False
    valHeart = 60
    if(valTouch):
        if(valUSRFB <= 3 or valUSRFT <= 3 or valUSRL <= 3 or valUSRR <= 3 or valIR > 1):
            digitalWrite(vibrator,1)
        else:
            digitalWrite(vibrator, 0)
        data["entries"] = makeData(
            valUSRFB, valUSRFT, valUSRL, valUSRR, valIR, valTouch, valHeart)
    return data
    
    


def getImages():
    directory = getcwd()
    # valUSRFB = round(converter(ultrasonicRead(usfb)), 1)
    # valUSRFT = round(converter(ultrasonicRead(usft)), 1)
    # valIR = round(irConverter(irDist()), 1)
    # takeImage(valUSRFB, valUSRFT, valIR)

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


def takeImage(fb, ft, ir):
    if(fb <= 3 or ft <= 3 or ir > 1):
        camera = PiCamera()

        camera.start_preview()
        print("Preview Stated")
        
        # Change image capture resoltion
        # max image size for pictures
        camera.resolution = (2592, 1944)  # keep 3:4 ratio
    
        # change frame rate (15 is max for this resoltion)
        camera.framerate = 15
        # rotate camera 180 degrees
        # camera.rotation = 180
        directory = getcwd()
        now = datetime.now()

        # dd/mm/YY H:M:S
        time = now.strftime("%d-%m-%Y-%H-%M-%S")
        filename = directory+'/src/assets/images/' +time +'.jpg'
        print(filename)
        camera.capture(filename)
        camera.stop_preview()
        print("Preview Ended")


def irDist():
    mySensor = qwiic_vl53l1x.QwiicVL53L1X()

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
    p.stopAsyncBPM
    return bpm
    


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
        digitalWrite(vibrator, 0)
        pool.terminate()


if __name__ == '__main__':
    runFile()
    digitalWrite(vibrator, 0)

   
