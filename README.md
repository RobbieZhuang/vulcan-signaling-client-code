# Vulcan Web Server in Flask and SocketIO
---
## Usage
All event names are under one root `/` namespace.
More example usage can be found in in `index.html`.

`'connect_host'`: Host sends their initial connection message to let the server know they exist

```
socket.emit('connect_host', {
    'msg': 'Connection request from the host'
});
```

`'connect_client'`: Client sends their initial connection message with a `room_id` field to connect to the room
```
socket.emit('connect_client', {
    'msg': 'Connection request from the client',
    'room_id': document.getElementById("party-room").value
});
```

`host_msg`: Let host forward a message (SDP, ICE) to the client
```
socket.emit('host_msg', {
    'client_id': document.getElementById("client-id").value,
    'msg': 'Message from the host'
});
```

`client_msg`: Let client forward a message (SDP, ICE) to the host
```
socket.emit('client_msg', {
    'msg': 'Message from the client'
});
```

## Packages Required

`pip3 install flask`

`pip3 install flask_socketio`

`pip3 install eventlet`


## Setting up in EC2

`tmux new -s testapp`
`tmux attach -t testapp`

`source env/bin/activate`

`pip3 install -r requirements.txt`

`export FLASK_APP=server.py`

`flask run --host=0.0.0.0 --port=8080`