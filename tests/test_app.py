import unittest
import flaskapi


# There are no separate tests for rates.py.  It is implicitly tested via
# calls from api.py.

class FlaskapiTestCase(unittest.TestCase):

    def setUp(self):
        flaskapi.app.testing = True
        self.app = flaskapi.app.test_client()

    def test_empty_db(self):
        response = self.app.get('/')
        assert response.status_code == 200
        assert b'Bob Goodfriend Flask API proof of concept' in response.data

    def test_rates(self):
        response = self.app.get('/rates/')
        assert response.status_code == 200
        assert b"[{'days': 'mon,tues,thurs', 'times': '0900-2100', 'tz': 'America/Chicago', 'price': 1500}, {'days': 'fri,sat,sun', 'times': '0900-2100', 'tz': 'America/Chicago', 'price': 2000}, {'days': 'wed', 'times': '0600-1800', 'tz': 'America/Chicago', 'price': 1750}, {'days': 'mon,wed,sat', 'times': '0100-0500', 'tz': 'America/Chicago', 'price': 1000}, {'days': 'sun,tues', 'times': '0100-0700', 'tz': 'America/Chicago', 'price': 925}]" in response.data

    # These next 2 more or less static endpoints I assume are working if they
    # respond 200.
    def test_swagger_endpoint(self):
        response = self.app.get('/swagger/')
        assert response.status_code == 200

    def test_metrics_endpoint(self):
        response = self.app.get('/metrics')
        assert response.status_code == 200

    def test_query_rates_get(self):
        response = self.app.get('query-rate?start_time=2015-07-01T07:00:00-05:00&end_time=2015-07-01T12:00:00-05:00')
        assert response.status_code == 200
        assert b'1750' in response.data

    def test_query_rates_get_with_missing_value(self):
        response = self.app.get('query-rate?end_time=2015-07-01T12:00:00-05:00')
        assert response.status_code == 400
        assert b'Please specify both start_time and end_time.' in response.data

    def test_query_rates_get_with_bogus_value(self):
        response = self.app.get('query-rate?start_time=bogus&end_time=2015-07-01T12:00:00-05:00')
        assert response.status_code == 400
        assert b'Bad format observed in start_time or end_time.' in response.data

    def test_query_rates_post(self):
        response = self.app.post('query-rate', json={
            'start_time': '2015-07-01T07:00:00-05:00',
            'end_time': '2015-07-01T12:00:00-05:00'
            })
        assert response.status_code == 200
        assert b'1750' in response.data

    def test_query_rates_post_with_missing_value(self):
        response = self.app.post('query-rate', json={
            'bogus': '2015-07-01T07:00:00-05:00',
            'end_time': '2015-07-01T12:00:00-05:00'
            })
        assert response.status_code == 400
        assert b'Please specify both start_time and end_time.' in response.data

    def test_query_rates_post_with_bad_value(self):
        response = self.app.post('query-rate', json={
            'start_time': 'bogus',
            'end_time': '2015-07-01T12:00:00-05:00'
            })
        assert response.status_code == 400
        assert b'Bad format observed in start_time or end_time.' \
            in response.data

    # Next test appears to be a single day, but spans 2 days after
    # accounting for local "tz": "America/Chicago"
    # It thus implicitly tests that function.
    def test_query_rates_return_unavailable(self):
        response = self.app.get('query-rate?start_time=2015-07-04T07:00:00%2B05:00&end_time=2015-07-04T20:00:00%2B05:00')
        assert response.status_code == 200
        assert b'unavailable' in response.data

    def test_set_rates(self):
        response = self.app.put('/setrates', json={'rates': [{'days': 'mon,tues,thurs', 'times': '0900-2100', 'tz': 'America/Chicago', 'price': 1500}, {'days': 'fri,sat,sun', 'times': '0900-2100', 'tz': 'America/New_York', 'price': 2000}, {'days': 'wed', 'times': '0600-1800', 'tz': 'America/Los_Angeles', 'price': 1750}, {'days': 'mon,wed,sat', 'times': '0100-0500', 'tz': 'America/Chicago', 'price': 1000}, {'days': 'sun,tues', 'times': '0100-0700', 'tz': 'America/Chicago', 'price': 925}]})
        assert response.status_code == 200
        assert b'OK' in response.data


if __name__ == '__main__':
    unittest.main()
