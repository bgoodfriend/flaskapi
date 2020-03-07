#!/usr/bin/env python

import flask
from flask import Flask, request, jsonify
import datetime
from flask_swagger_ui import get_swaggerui_blueprint
from prometheus_flask_exporter import PrometheusMetrics

# Local files
from flaskapi.rates import rates, check_rates

app = Flask(__name__)
metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Application info', version='1.0.0')
# app.config["DEBUG"] = True

# create swagger UI
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
# end swagger UI


@app.route('/', methods=['GET'])
def home():
    pass
    return "<h1>Bob Goodfriend Flask API proof of concept</h1>"


@app.route('/rates/', methods=['GET'])
def api_front():
    pass
    return jsonify(rates)


@app.route('/setrates', methods=['PUT'])
def set_rates():
    # "10. The application publishes a second API endpoint where rate
    # information can be updated by submitting a modified rates JSON and
    # can be stored in memory"
    req = request.get_json()

    global rates
    rates = req['rates']
    pass
    return "OK"


@app.route('/query-rate', methods=['GET', 'POST'])
def query_rate():
    # Dates are in ISO-8601 format with time offset.  They look like eg.
    # 2015-07-04T20:00:00+00:00
    query_date_format = "%Y-%m-%dT%H:%M:%S%z"

    if flask.request.method == 'GET':
        query_start_time = datetime.datetime.strptime(request.args.get('start_time'), query_date_format)
        query_end_time = datetime.datetime.strptime(request.args.get('end_time'), query_date_format)
    else:
        query_start_time = datetime.datetime.strptime(request.json['start_time'], query_date_format)
        query_end_time = datetime.datetime.strptime(request.json['end_time'], query_date_format)

    return check_rates(query_start_time, query_end_time)


metrics.register_default(
    metrics.counter(
        'by_path_counter', 'Request count by request paths',
        labels={'path': lambda: request.path}
    )
)

# app.run(host='0.0.0.0')
