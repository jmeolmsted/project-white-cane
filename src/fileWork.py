from os import listdir
from os.path import isfile, join
try:
    import simplejson as json
except:
    import json

import sys

from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify

onlyfiles = [f for f in listdir('C:/Users/jimmi/Desktop/IOT_Walking_Stick/src/assets/images') if isfile(
    join('C:/Users/jimmi/Desktop/IOT_Walking_Stick/src/assets/images', f))]

count = 0
out = {'files': []}


def makeEntry(k,v):
    return {'id': k, 'name': v}

for x in onlyfiles:
    key = count
    value = x
    out["files"].append(makeEntry(key,value))
    count+=1

app = Flask(__name__)
api = Api(app)

CORS(app)

@app.route("/")
def hello():
    return jsonify({'text':'Hello World!'})

class Files(Resource):
    def get(self):
        return out    


api.add_resource(Files, '/files') # Route_1


if __name__ == '__main__':
     app.run(port=5002)
