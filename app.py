import socketio  # socket-io library
import eventlet
from flask import Flask # web.py framework for hosting webpages
import mdc_api 			# mbed Device Connector library
import pybars 			# use to fill in handlebar templates

sio = socketio.Server()
app = Flask(__name__)


token = "ChangeMe" # replace with your API token
connector = mdc_api.connector(token)
connector.startLongPolling()

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
	sio.enter_room(sid,'globalRoom')

@sio.on('subscribe_to_presses')
def subscribeToPresses(sid, data):
    print('subscribe_to_presses: ',sid, data)	

@sio.on('unsubscribe_to_presses')
def unsubscribeToPresses(sid, data):
    print('unsubscribe_to_presses: ',sid, data)
    
@sio.on('get_presses')
def getPresses(sid, data):
	# Read data from GET resource /3200/0/5501 (num button presses)
	print("get_presses ",sid,data)
	e = connector.getResourceValue(data['endpointName'],'/3200/0/5501')
	while not e.isDone():
		None
	if e.error:
		print("Error: ",e.error.errType, e.error.error, e.raw_data)
	else:
		sio.emit('presses',{"endpointName":data['endpointName'],"value":e.result},room='globalRoom')
    
@sio.on('update_blink_pattern')
def updateBlinkPattern(sid, data):
	# Set data on PUT resource /3201/0/5853 (pattern of LED blink)
    print('update_blink_pattern ',sid, data)
    e = connector.putResourceValue(data['endpointName'],'/3201/0/5853',data['blinkPattern'])
    while not e.isDone():
    	None
    if e.error:
	    print("Error: ",e.error.errType, e.error.error, e.raw_data)
    	

@sio.on('blink')
def blink(sid, data):
	# Trigger POST resource /3201/0/5850 (start blinking LED)
    print('blink: ',sid, data)
    e = connector.postResource(data['endpointName'],'/3201/0/5850')
    while not e.isDone():
    	None
    if e.error:
    	print("Error: ",e.error.errType, e.error.error, e.raw_data)

# 'notifications' are routed here
def notificationHandler(data):
	print "\r\nNotification Data Received :\r\n %s" %data['notifications']

if __name__ == "__main__":
	app = socketio.Middleware(sio, app)							# wrap Flask application with socketio's middleware
	eventlet.wsgi.server(eventlet.listen(('', 8080)), app) 		# deploy as an eventlet WSGI server
	#connector.startLongPolling()								# start long polling connector.mbed.com
	connector.setHandler('notifications', notificationHandler) 	# send 'notifications' to the notificationHandler FN