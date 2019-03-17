'''
Sensehat Dashboard w/ Firebase
------------------------------------
LED Matrix application
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
  'databaseAuthVariableOverride': {
    'uid': 'ambilight'
  }
})

# Create instance of firestore
db =  firestore.client()

# Function to set pixels
def setPixels(state, color):
  if(state == 'on'):
    color = color.lstrip('#')
    color_pixel = tuple(int(color[i:i+2], 16) for i in (0, 2 ,4))
    for x in range(0,8):
      for y in range(0,8):
        sense.set_pixel(x, y, color_pixel)
  else:
    sense.clear()


# Callback function
def on_snapshot(doc_snapshot, changes, read_time):
  print(u'Received document snapshot: {}'.format(doc_snapshot[0].id))
  color_doc = doc_snapshot[0]
  color_data = color_doc.to_dict()
  state = color_data['state']
  color_hex = color_data['value']
  setPixels(state, color_hex)



# Activate listener thread
@app.before_first_request
def activate_listener():
  def run_listener():
    doc_watch = db.collection(u'pi').document(u'color').on_snapshot(on_snapshot)
  thread = threading.Thread(target=run_listener)
  thread.daemon = True
  thread.start()

@app.route('/')
def hello():
  return 'General Kenobi!'

def start_runner():
  def start_loop():
    not_started = True
    while not_started:
      print('In start loop')
      try:
        r = requests.get('http://192.168.0.205:8081/')
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

if __name__ == '__main__':
  start_runner()
  app.run(host = '192.168.0.205', port = 8081, debug = True, use_reloader=False)