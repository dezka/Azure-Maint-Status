#!/usr/bin/python
''' 
Description:
 * This is a Flask app that when hit on :8088, it will hit the Azure Instance Metadata Service which is sitting
   on the APIPA address space for the Instance this is running on. If the length of the JSON result is 0, then a
   200 OK is returned. Else a 503 HTTP code is returned.

   This was hooked up originally to an Orion Solarwinds system which was looking for a 200 OK, and would alert on a 503.

Authors:
 * Dennis T Bielinski
'''

import requests
import logging
import os
import sys
import time

from flask_api import status
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from logging.handlers import RotatingFileHandler

file_path_base = os.path.splitext(__file__)[0]

# Flask logs accesses to stderr (?)
sys.stderr = open('/var/log/AzureStatus/' + 'AzureStatus.stderr', 'a')

app = Flask(__name__)

# INFO: It seems flask won't output your debug logs in debug mode.
#       This is stupid, so to confuse less people, it's never on.
app.debug = False

class Formatter(logging.Formatter):
    """Basically adds a better, automatic timestamp to the log"""
    def format(self, record):
        time = self.formatTime(record)
        message = logging.Formatter.format(self, record)

        return '[{0}] {1}'.format(time, message)

    def formatTime(self, record, datefmt=None):
        if datefmt is not None:
            return time.strftime(datefmt)
        else:
            return str(datetime.utcnow()).replace(' ', 'T') + 'Z'

# Set up logging for the app

log_file_handler = RotatingFileHandler('/var/log/AzureStatus/' + 'AzureStatus.log', maxBytes=1048576, backupCount=100)
log_file_handler.setLevel(logging.INFO)
log_file_handler.setFormatter(Formatter())

app.logger.addHandler(log_file_handler)

# Set up the routes

@app.route('/maint')
def getstatus():
    time.sleep(1)
    r = requests.get('http://169.254.169.254/metadata/v1/maintenance')
    lookup = r.json()
    if len(lookup) == 0:
        return '200 OK', 200
    else:
        return str(status.HTTP_503_SERVICE_UNAVAILABLE), 503

@app.after_request
def write_access_log(response):
    message = '{0} {1} {2}'.format(request.method, request.url, response.status)
    app.logger.info(message)

    return response

if __name__ == '__main__':
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(8088)
    IOLoop.instance().start()
