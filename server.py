from party import *
from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room
import json
import uuid

app = Flask('web_server')

socketio = SocketIO(app, cors_allowed_origins='*')


### Global Variables
# Stores all parties in a dictionary keyed by `party_id`
parties = dict()
host_to_party = dict()
client_to_host = dict()


### HTML page rendering 
@app.route('/')
def root_page():
	return render_template('index.html')


#### Helper functions
def generate_id():
	return str(uuid.uuid1())


### SocketIO Event Handlers
# General connection
@socketio.on('connect')
def connected():
	print('client connected')

# Forward message from host to a specified client
@socketio.on('host_msg')
def handle_host_msg(msg):
	host_id = request.sid
	
	# Check if host exists
	if host_id not in host_to_party:
		return
	
	# Forward host's message to the client
	client_id = msg['client_id']

	# Check if client is in the party for that host
	if client_id not in parties[host_to_party[host_id]].get_client_ids():
		return 
	
	socketio.emit('client_msg', f'{msg}', room = client_id)


# Forward message from client to a specified host
@socketio.on('client_msg')
def handle_client_msg(msg):
	client_id = request.sid

	# Check if client exists
	if client_id not in client_to_host:
		return

	host_id = client_to_host[client_id]

	socketio.emit('host_msg', f'{msg}', room = host_id)


@socketio.on('connect_client')
def handle_client_connect(msg):

	def notify_host_of_client(client_id, host_id):
		data = {'id' : client_id, 'type' : 'new'}
		socketio.emit('new_client', json.dumps(data), json = True, room = host_id)

	party_id = msg['room_id']

	# Check if the party exists
	if party_id not in parties.keys():
		socketio.emit('connect_client', f'Party doesn\'t exist: {party_id}')
		return
	
	# Get the id for the client
	client_id = request.sid

	# Send client to a room
	join_room(client_id)

	# Add client to party
	parties[party_id].add_client(client_id)

	party_host_id = parties[party_id].get_host_id() 

	client_to_host[client_id] = party_host_id

	# Join 
	socketio.emit('connect_client', f'You have joined host\'s room: {party_host_id}', room = client_id)

	# Notify the host of the new client
	notify_host_of_client(client_id, party_host_id)
	
@socketio.on('connect_host')
def handle_host_connect(msg):
	# Generate an id for the host
	host_id = request.sid
	
	# Generate an id for the party
	party_id = generate_id()

	# Create a socketio room containing only the host
	join_room(host_id)
	
	# Create a party
	party = Party(party_id, host_id)

	# Add the party to the global parties dict
	parties[party_id] = party
	host_to_party[host_id] = party_id

	data = {'partyid' : party_id, 'hostid' : host_id}
	
	# Send party ID back to the host
	socketio.emit('connect_host', json.dumps(data), room = host_id)

if __name__=='__main__':
	try:
		app.run()
		print('Signalling server started')
		socketio.run(app, host='0.0.0.0')
	except:
		pass