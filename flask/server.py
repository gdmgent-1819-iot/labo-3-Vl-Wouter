'''
Sensehat Dashboard
--------------------
Author: drdynscript
Modified: 03-12-2019
--------------------
Installation:
sudo pip3 -U Flask
Docs: http://flask.pocoo.org/docs/1.0/
'''
# Import the libraries
from flask import Flask, jsonify, render_template, request
from sense_hat import SenseHat

# Create an instance of flask
app = Flask(__name__)

# Create an instance of the sensehat
sense = SenseHat()

# Function to send colors to sensehat
def setColor(color_data):
	if color_data['state'] == 'on':
		color = color_data['value'].lstrip('#')
		rgb = tuple(int(color[i:i+2], 16) for i in (0, 2 ,4))
		for x in range(0,8):
			for y in range(0,8):
				sense.set_pixel(x, y, rgb)
	else:
		for x in range(0,8):
			for y in range(0,8):
				sense.set_pixel(x, y, [0, 0, 0])

# Define the root route
@app.route('/')
def index():
  return 'Look the flask server is running'

# Define the nmd route
@app.route('/nmd')
def nmd():
  return 'Greetings Earthlings. We are NMDrs'

# Define the my_ip route
@app.route('/my_ip', methods=['GET'])
def my_ip():
  return jsonify({
    'ip': request.remote_addr
  }), 200

# Define the api_environment route
@app.route('/api/environment', methods=['GET'])
def api_environment():
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
  return jsonify(environment_obj), 200

@app.route('/ambilight', methods=['GET', 'POST'])
def ambilight():
	if request.method == 'POST':
		print('POST')
		data = request.form
		print(data)
		color_val = data['color']
		print(color_val)
		if 'on_off' in data and data['on_off'] == 'on':
			state = 'on'
		else:
			state = 'off'
	else:
		color_val = '#ffffff'
		state = 'off'

	color_data = {
		'value': color_val,
		'state': state,
	}
	setColor(color_data)
	return render_template('ambilight.html', color=color_data)

# Define the api_environment route
@app.route('/environment', methods=['GET'])
def environment():
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
  return render_template('environment.html', environment=environment_obj)

# Main method for Flask server
if __name__ == '__main__':
  app.run(host = '10.5.129.10', port = 8080, debug = True)