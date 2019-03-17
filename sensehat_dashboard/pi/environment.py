'''
Sensehat Dashboard w/ Firebase
------------------------------------
Environment Sensor application
------------------------------------
Author: Vl-Wouter
Modified: 03-16-2019
'''

import requests
import threading
import time
from flask import Flask
import firebase_admin
from firebase_admin import credentials, firestore
from sense_hat import SenseHat

# Create instance of Flask
app = Flask(__name__)

# Create instance of sensehat
sense = SenseHat()

# Create instance of firebase
cred = credentials.Certificate('./credentials.json')
environment_app = firebase_admin.initialize_app(cred, {
  'databaseURL': 'https://pi-server-cc2b0.firebaseio.com/',
  'databaseAuthVariableOverride': {
    'uid': 'environment_updater'
  }
})

# Create instance of firestore
db = firestore.client()

# Activate update thread before request is made
@app.before_first_request
def activate_update():
  def run_job():
    while True:
      print('Updating DB')
      environment_obj = {
        'temperature': {
          'value': round(sense.get_temperature()),
          'unit': u'C'
        },
        'humidity': {
          'value': round(sense.get_humidity()),
          'unit': u'%'
        },
        'pressure': {
          'value': round(sense.get_pressure()),
          'unit': u'mbar'
        }
      }
      db.collection('pi').document('environment').set(environment_obj)
      time.sleep(120)
  thread = threading.Thread(target=run_job)
  thread.daemon = True
  thread.start()

# Have something on this route
@app.route('/')
def hello():
  return 'Hello there!'

# Runner to start server and update thread
def start_runner():
  def start_loop():
    not_started = True
    while not_started:
      print('In start loop')
      try:
        r = requests.get('http://192.168.0.205:8080/')
        if r.status_code == 200:
          print('Server started: quitting start_loop')
          not_started = False
        print(r.status_code)
      except:
        print('Server not yet started')
      time.sleep(2)
  print('Started runner')
  thread = threading.Thread(target=start_loop)
  thread.daemon = True
  thread.start()

# Main method for the Flask server
if __name__ == '__main__':
  start_runner()
  app.run(host = '192.168.0.205', port = 8080, debug = True, use_reloader=False)