from flask import Flask
app = Flask(__name__)

from flaskapi import api

if __name__ == '__main__':
    app.run()
