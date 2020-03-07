#!/usr/bin/env python

import os
import unittest
import tempfile
import flaskapi

class FlaskapiTestCase(unittest.TestCase):

    def setUp(self):
        flaskapi.app.testing = True
        self.app = flaskapi.app.test_client()

    def test_empty_db(self):
        response = self.app.get('/')
        assert response.status_code == 200
        assert b'Bob Goodfriend Flask API proof of concept' in response.data

if __name__ == '__main__':
    unittest.main()

