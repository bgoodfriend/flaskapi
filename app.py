#!/usr/bin/env python

import json
import flask
from flask import Flask, request, jsonify
import datetime
from pytz import timezone
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
app.config["DEBUG"] = True

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Bob Goodfriend Flask API proof of concept"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###

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

def check_rates( query_start_time, query_end_time ):
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

    for rate in rates:
        # "7. User input can span more than one day, but the API shouldn't
        # return a valid rate"
        # Note: Whether a date range spans multiple days can depend on if you
        # calculate it relative to its submitted tz or the rate bucket's tz.
        # For purposes of matching a rate, it makes sense to do the latter

        if query_start_time.astimezone(timezone(rate["tz"])).weekday() != query_end_time.astimezone(timezone(rate["tz"])).weekday():
            #Timezone days don't match: skip.
            continue;

        [ rate_start_time, rate_end_time ] = rate["times"].split('-')
        for day_of_week in rate["days"].split(','):
            if query_start_time.astimezone(timezone(rate["tz"])).weekday() != weekdays[day_of_week]:
                #Query weekdays don't match in this tz: skip.
                continue

            if query_start_time.astimezone(timezone(rate["tz"])).strftime("%H%M") < rate_start_time:
                #Query start time before bucket start time: skip
                continue
            if query_end_time.astimezone(timezone(rate["tz"])).strftime("%H%M") > rate_end_time:
                #Query end time after bucket end time: skip
                continue

            # If you reached here, this is a match.
            return str(rate["price"])
    # If you got this far, you went through every bucket without a match
    return "unavialable"

@app.route('/', methods=['GET'])
def home():
    return "<h1>Bob Goodfriend Flask API proof of concept</h1>"

@app.route('/rates/', methods=['GET'])
def api_front():
    return jsonify(rates)

@app.route('/setrates', methods=['PUT'])
def set_rates():
    # "10. The application publishes a second API endpoint where rate 
    # information can be updated by submitting a modified rates JSON and 
    # can be stored in memory"
    req = request.get_json()

    global rates
    rates = req['rates']
    return "Thanks!"

@app.route('/query-rate', methods=['GET', 'POST'])
def query_rate():
    # Dates are in ISO-8601 format with time offset.  They look like eg.
    # 2015-07-04T20:00:00+00:00
    query_date_format = "%Y-%m-%dT%H:%M:%S%z"

    if flask.request.method == 'GET':
        query_start_time = datetime.datetime.strptime( request.args.get('start_time'), query_date_format )
        query_end_time = datetime.datetime.strptime( request.args.get('end_time'), query_date_format )
    else:
        query_start_time = datetime.datetime.strptime( request.json['start_time'], query_date_format )
        query_end_time = datetime.datetime.strptime( request.json['end_time'], query_date_format )

    return check_rates( query_start_time, query_end_time )

app.run(host='0.0.0.0')


