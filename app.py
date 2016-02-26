# Steps to get this running
# 1) run `sudo pip install -U requests[security] web.py` to install ssl capablities and the web.py framework
# 2) install the mbed connector module (TODO: publish it and make it not copy / paste)
# 3) Share the project app externally (top right corner, Share-> Application -> [*] Public
# 4) Put in API token from https://connector.mbed.com/#accesskeys
# 5) Run app
# 6) Go to the address that pops up to see it run!
import socketio  # socket-io library
import eventlet
from flask import Flask # web.py framework for hosting webpages
import mdc_api 			# mbed Device Connector library
import pybars 			# use to fill in handlebar templates

sio = socketio.Server()
app = Flask(__name__)


token = "Change Me" # replace with your API token
connector = mdc_api.connector(token)

@app.route('/')
def index():
	# get list of endpoints, for each endpoint get the pattern (/3201/0/5853) value
	epList = connector.getEndpoints().result
	for index in range(len(epList)):
		print epList[index]['name']
		e = connector.getResourceValue(epList[index]['name'],"/3201/0/5853")
		while not e.isDone():
			None
		epList[index]['blinkPattern'] = e.result
	print epList
	#epList = {'endpoints':[{'name':'test1','blinkPattern':'500:500:500:600'},{'name':'test2','blinkPattern':'panumba'}]}
	
	# fill out html using handlebar template
	handlebarJSON = {'endpoints':epList}
	comp = pybars.Compiler()
	source = unicode(open("./views/index.hbs",'r').read())
	template = comp.compile(source)
	return "".join(template(handlebarJSON))

@sio.on('connect')
def connect(sid, environ):
    print('connect ', sid)

@sio.on('subscribe-to-presses')
def subscribeToPresses(sid, data):
    print('subscribe-to-presses: ', data)	

@sio.on('unsubscribe-to-presses')
def unsubscribeToPresses(sid, data):
    print('unsubscribe-to-presses: ', data)
    
@sio.on('get-presses')
def getPresses(sid, data):
    print('get-presses ', data)
    
@sio.on('update-blink-pattern')
def updateBlinkPattern(sid, data):
    print('message ', data)

@sio.on('blink')
def blink(sid, data):
    print('blink: ', data)

# 'notifications' are routed here
def notificationHandler(data):
	print "\r\nNotification Data Received :\r\n %s" %data['notifications']

if __name__ == "__main__":
	app = socketio.Middleware(sio, app)							# wrap Flask application with socketio's middleware
	eventlet.wsgi.server(eventlet.listen(('', 8080)), app) 		# deploy as an eventlet WSGI server
	connector.startLongPolling()								# start long polling connector.mbed.com
	connector.setHandler('notifications', notificationHandler) 	# send 'notifications' to the notificationHandler FN