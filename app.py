import socketio  # socket-io library
import eventlet
from flask import Flask # web.py framework for hosting webpages
import mdc_api 			# mbed Device Connector library
import pybars 			# use to fill in handlebar templates
from base64 import standard_b64decode as b64decode

sio = socketio.Server()
app = Flask(__name__)

g_sid = ""

token = "ChangeMe" # replace with your API token
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
	global g_sid
	print('connect ', sid)
	sio.enter_room(sid,'globalRoom')
	g_sid = sid

@sio.on('subscribe_to_presses')
def subscribeToPresses(sid, data):
	# Subscribe to all changes of resource /3200/0/5501 (button presses)
	print('subscribe_to_presses: ',sid, data)
	e = connector.putResourceSubscription(data['endpointName'],'/3200/0/5501')
	while not e.isDone():
		None
	if e.error:
		print("Error: ",e.error.errType, e.error.error, e.raw_data)
	else:
		print("Subscribed Successfully!")
		sio.emit('subscribed-to-presses',{"endpointName":data['endpointName'],"value":'True'})

@sio.on('unsubscribe_to_presses')
def unsubscribeToPresses(sid, data):
	print('unsubscribe_to_presses: ',sid, data)
	e = connector.deleteResourceSubscription(data['endpointName'],'/3200/0/5501')
	while not e.isDone():
		None
	if e.error:
		print("Error: ",e.error.errType, e.error.error, e.raw_data)
	else:
		print("Unsubscribed Successfully!")
		sio.emit('unsubscribed-to-presses',{"endpointName":data['endpointName'],"value":'True'})
    
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
		data_to_emit = {"endpointName":data['endpointName'],"value":e.result}
		print data_to_emit
		sio.emit('presses', data_to_emit,room='globalRoom')
    
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
	notifications = data['notifications']
	constructedList = {}
	for thing in notifications:
		ep = thing['ep']
		emit = {"endpointName":thing["ep"],"value":b64decode(thing["payload"])}
		print emit
		print str(g_sid)
		sio.emit('presses',emit,room=str(g_sid))

if __name__ == "__main__":
	connector.deleteAllSubscriptions()
	connector.startLongPolling()								# start long polling connector.mbed.com
	connector.setHandler('notifications', notificationHandler) 	# send 'notifications' to the notificationHandler FN
	app = socketio.Middleware(sio, app)							# wrap Flask application with socketio's middleware
	eventlet.wsgi.server(eventlet.listen(('', 8080)), app) 		# deploy as an eventlet WSGI server
	