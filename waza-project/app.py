from flask import Flask, request, jsonify, abort
import config
from model.meeting import Meeting
from model.room import Room

app = Flask(__name__)

#------------------------------------
# app routes for Meeting
#------------------------------------
@app.route('/waza/meeting/', methods=['POST', 'GET'])
def meetings():
    connection = config.connection
    if request.method == "POST":
        created_by = request.form.get('created_by', '')
        room_id = request.form.get('room_id', '')
        start_at = request.form.get('start_at', '')
        end_at = request.form.get('end_at', '')
        meet_id = Meeting.post(connection, created_by, room_id, start_at, end_at)
        return {
            "message": ("Meeting with id %s was inserted" % (meet_id))
        }, 200
    else:
        response = jsonify(Meeting.get_all(connection))
        response.status_code = 200
        return response


@app.route('/waza/meeting/<int:meeting_id>', methods=['DELETE', 'GET', 'PUT'])
def meetings_detail(meeting_id):
    connection = config.connection
    meet = Meeting.get_first(connection, meeting_id)
    if not meet:
        abort(404)

    if request.method == 'DELETE':
        Meeting.delete(connection, meet["id"])
        return {
            "message": ("Meeting with id %s was removed" % (meet["id"]))
        }, 200

    elif request.method == 'PUT':
        created_by = request.form.get('created_by', '')
        room_id = request.form.get('room_id', '')
        start_at = request.form.get('start_at', '')
        end_at = request.form.get('end_at', '')
        Meeting.put(connection, meet["id"], created_by, room_id, start_at, end_at)
        return {
            "message": ("Meeting with id %s was updated" % (meet["id"]))
        }, 200

    else:
        return meet

#------------------------------------
# app routes for Room
#------------------------------------

@app.route('/waza/room/', methods=['POST', 'GET'])
def room():
    connection = config.connection
    if request.method == "POST":
        roomtype_id = request.form.get('roomtype_id', '')
        department_id = request.form.get('department_id', '')
        name = request.form.get('name', '')
        capacity = request.form.get('capacity', '')
        room_id = Room.post(connection, roomtype_id, department_id, name, capacity)
        return {
            "message": ("Room with id %s was inserted" % (room_id))
        }, 200
    else:
        response = jsonify(Room.get_all(connection))
        response.status_code = 200
        return response


@app.route('/waza/room/<int:room_id>', methods=['DELETE', 'GET', 'PUT'])
def room_detail(room_id):
    connection = config.connection
    room = Room.get_first(connection, room_id)
    if not room:
        abort(404)

    if request.method == 'DELETE':
        Room.delete(connection, room["id"])
        return {
            "message": ("Room with id %s was removed" % (room["id"]))
        }, 200

    elif request.method == 'PUT':
        roomtype_id = request.form.get('roomtype_id', '')
        department_id = request.form.get('department_id', '')
        name = request.form.get('name', '')
        capacity = request.form.get('capacity', '')
        Meeting.put(connection, room["id"], roomtype_id, department_id, name, capacity)
        return {
            "message": ("Room with id %s was updated" % (room["id"]))
        }, 200

    else:
        return room

if __name__ == '__main__':
    app.run()
