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

    # A rate bucket looks like:
    #         {
    #        "days": "mon,tues,thurs",
    #        "times": "0900-2100",
    #        "tz": "America/Chicago",
    #        "price": 1500
    #    },
    # NOTE "days' uses a string of nonstandard abbreviations, therefore
    # requiring the following translator:
    weekdays = { "mon":0, "tues":1, "wed":2, "thurs":3, 
            "fri":4, "sat":5, "sun":6 }

    query_start_time = datetime.datetime.strptime( request.args.get('start_time'), "%Y-%m-%dT%H:%M:%S%z" )
    query_end_time = datetime.datetime.strptime( request.args.get('end_time'), "%Y-%m-%dT%H:%M:%S%z" )
    print(query_start_time.isoformat())
    print(query_end_time.isoformat())

    for rate in rates:
        # "7. User input can span more than one day, but the API shouldn't 
        # return a valid rate"
        # Note: Whether a date range spans multiple days can depend on if you
        # calculate it relative to its submitted tz or the rate bucket's tz.
        # For purposes of matching a rate, it makes sense to do the latter
        #print(query_start_time.astimezone(timezone(rate["tz"])).isoformat())
        #print(query_end_time.astimezone(timezone(rate["tz"])).isoformat())
        if query_start_time.astimezone(timezone(rate["tz"])).weekday() != query_end_time.astimezone(timezone(rate["tz"])).weekday():
            #Timezone days don't match, skipping.
            continue;
        print("Timezone days matched.")

        [ rate_start_time, rate_end_time ] = rate["times"].split('-')
        print(rate_start_time, rate_end_time)
        print(query_start_time.astimezone(timezone(rate["tz"])).weekday())
        print(query_end_time.astimezone(timezone(rate["tz"])).weekday())
        #print(rate["days"].split(','))
        for day_of_week in rate["days"].split(','):
            print(day_of_week)
            #print(weekdays[day_of_week])
            if query_start_time.astimezone(timezone(rate["tz"])).weekday() != weekdays[day_of_week]:
                #Weekdays don't match, skipping.
                continue
            print("matched weekday.")
            print(query_start_time.astimezone(timezone(rate["tz"])).strftime("%H%M"))
            print(query_end_time.astimezone(timezone(rate["tz"])).strftime("%H%M"))
            if query_start_time.astimezone(timezone(rate["tz"])).strftime("%H%M") < rate_start_time:
                print("query start before bucket start")
                continue
            if query_end_time.astimezone(timezone(rate["tz"])).strftime("%H%M") > rate_end_time:
                print("query end time after bucket end time")
                continue
            print("MATCHED")
            print(rate["price"])
        
    return '''<h1>The start time value is: {}</h1>
              <h1>The end time value is:   {}</h1>'''.format(query_start_time.isoformat(), query_end_time.isoformat())

app.run(host='0.0.0.0')
