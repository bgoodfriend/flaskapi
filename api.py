#!/usr/bin/env python

import json
import flask
from flask import request, jsonify
import datetime
import dateutil.parser
from pytz import timezone
from tzlocal import get_localzone

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
        "tz": "America/Los_Angeles",
        "price": 2000
    },
    {
        "days": "wed",
        "times": "0600-1800",
        "tz": "America/New_York",
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
    return "<h1>Flask basic API example</h1><p>This site implements a GET, query via GET, and a POST.</p>"

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
    # Dates are in ISO-8601 format with time offset.  They look like eg.
    # 2015-07-04T20:00:00+00:00
    start_time = datetime.datetime.strptime( request.args.get('start_time'), "%Y-%m-%dT%H:%M:%S%z" )
    end_time = datetime.datetime.strptime( request.args.get('end_time'), "%Y-%m-%dT%H:%M:%S%z" )
    print(start_time.isoformat())
    print(end_time.isoformat())

    # Chicago specific
    #print(start_time.astimezone(timezone('America/Chicago')).isoformat())
    #print(start_time.astimezone(timezone('America/Chicago')).weekday())
    #print(start_time.astimezone(timezone('America/Chicago')).hour)

    for rate_dict in rates:
        print(rate_dict["tz"])
        # "7. User input can span more than one day, but the API shouldn't 
        # "return a valid rate"
        # Note: Whether a date range spans multiple days can depend on if you
        # calculate it relative to its submitted tz or the rate bucket's tz.
        # For purposes of matchign a rate, it makes sense to do the latter
        print(start_time.astimezone(timezone(rate_dict["tz"])).isoformat())
        print(end_time.astimezone(timezone(rate_dict["tz"])).isoformat())
        #if first != second:
        if start_time.astimezone(timezone(rate_dict["tz"])).weekday() != end_time.astimezone(timezone(rate_dict["tz"])).weekday():
            print("Days don't match, skipping.")
            continue;
        print("Days matched.")
        print(rate_dict["days"].split(','))
        for day_of_week in rate_dict["days"].split(','):
            print(day_of_week)
        
    return '''<h1>The start time value is: {}</h1>
              <h1>The end time value is:   {}</h1>'''.format(start_time.isoformat(), end_time.isoformat())

app.run(host='0.0.0.0')
