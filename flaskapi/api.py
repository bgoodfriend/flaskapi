import flask
# from flask import request, jsonify
from flask import request
import datetime
from flask_swagger_ui import get_swaggerui_blueprint
from prometheus_flask_exporter import PrometheusMetrics

# Local
from flaskapi import app
from flaskapi.rates import rates, check_rates

metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Application info', version='1.0.0')
app.config["DEBUG"] = True

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
    return "<h1>Bob Goodfriend Flask API proof of concept</h1>"


@app.route('/rates/', methods=['GET'])
def api_front():
    # return jsonify(rates)
    # return_str = ', '.join(rates)
    print(str(rates))
    return str(rates)


@app.route('/setrates', methods=['PUT'])
def set_rates():
    req = request.get_json()

    global rates
    rates = req['rates']
    return "OK"


@app.route('/query-rate', methods=['GET', 'POST'])
def query_rate():
    # Dates are in ISO-8601 format with time offset.  They look like eg.
    # 2015-07-04T20:00:00+00:00
    query_date_format = "%Y-%m-%dT%H:%M:%S%z"

    gotValidDates = None
    if flask.request.method == 'GET':
        if request.args.get('start_time') is None \
                or request.args.get('end_time') is None:
            return "Please specify both start_time and end_time.", 400

        try:
            query_start_time = datetime.datetime.strptime(
                request.args.get('start_time'), query_date_format)
            query_end_time = datetime.datetime.strptime(
                request.args.get('end_time'), query_date_format)
        except ValueError:
            gotValidDates = False
    else:
        req = request.get_json()

        if 'start_time' not in req or 'end_time' not in req:
            return "Please specify both start_time and end_time.", 400

        try:
            query_start_time = datetime.datetime.strptime(
                req['start_time'], query_date_format)
            query_end_time = datetime.datetime.strptime(
                req['end_time'], query_date_format)
        except ValueError:
            gotValidDates = False

    if gotValidDates is False:
        return "Bad format observed in start_time or end_time.", 400

    return check_rates(query_start_time, query_end_time)


metrics.register_default(
    metrics.counter(
        'by_path_counter', 'Request count by request paths',
        labels={'path': lambda: request.path}
    )
)
