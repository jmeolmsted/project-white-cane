from os import listdir, getcwd
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

import socket

ip = socket.gethostbyname(socket.gethostname())
app = Flask(__name__)
api = Api(app)

CORS(app)

@app.route("/")
def hello():
    return jsonify({'text':'Hello World!'})

class ipAddress(Resource):
    def get(self):
        return jsonify({'ip': ip})   


api.add_resource(ipAddress, '/ipAddress') # Route_1


if __name__ == '__main__':
     app.run(port=5002)