#!/usr/bin/env python

import json
import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

### Default rates.  
rates = [
    {
        "days": "mon,tues,thurs",
        "times": "0900-2100",
        "tz": "America/Chicago",
        "price": 1500
    },
    {
        "days": "fri,sat,sun",
        "times": "0900-2100",
        "tz": "America/Chicago",
        "price": 2000
    },
    {
        "days": "wed",
        "times": "0600-1800",
        "tz": "America/Chicago",
        "price": 1750
    },
    {
        "days": "mon,wed,sat",
        "times": "0100-0500",
        "tz": "America/Chicago",
        "price": 1000
    },
    {
        "days": "sun,tues",
        "times": "0100-0700",
        "tz": "America/Chicago",
        "price": 925
    }
]

@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

# A route to return all of the available entries in our catalog.
@app.route('/rates/', methods=['GET'])
def api_all():
    return jsonify(rates)

@app.route('/setrates', methods=['POST'])
def set_rates():
    req = request.get_json()

    global rates
    rates = req['rates']
    print(rates)
    return "Thanks!"

@app.route('/query-rate')
def query_rate():
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    return '''<h1>The start time value is: {}</h1>
              <h1>The end time value is:   {}</h1>'''.format(start_time, end_time)

app.run(host='0.0.0.0')
