from os import listdir
from os.path import isfile, join
try:
    import simplejson as json
except:
    import json

import sys

from flask import Flask, render_template, request, redirect, Response
import random, json

onlyfiles = [f for f in listdir('C:/Users/jimmi/Desktop/IOT_Walking_Stick/src/assets/images') if isfile(
    join('C:/Users/jimmi/Desktop/IOT_Walking_Stick/src/assets/images', f))]

count = 0
out = {'list': []}


def makeEntry(k, v):
    return {k:v}

for x in onlyfiles:
    key = "key{:d}".format(count)
    value = x
    out["list"].append(makeEntry(key,value))

print (json.dumps(out))

app = Flask(__name__)

@app.route('/')
def output():
	# serve index template
	return render_template('index.html', name='Joe')

@app.route('/receiver', methods = ['POST'])
def worker():
	# read json + reply
	data = request.get_json(force=True)
	result = ''

	for item in data:
		# loop over every row
		make = str(item['make'])
		if(make == 'Porsche'):
			result += make + ' -- That is a good manufacturer\n'
		else:
			result += make + ' -- That is only an average manufacturer\n'

	return result

if __name__ == '__main__':
	# run!
	app.run()
