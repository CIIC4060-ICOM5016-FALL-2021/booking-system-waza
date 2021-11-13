from flask_cors import CORS
from flask import Flask, request, jsonify, abort
from controller.meeting import BaseMeeting
from controller.invitee import BaseInvitee
from controller.user import BaseUser
from model.room import Room

# Remove this line and file after removing dependencies to it
import tbd_config
#

app = Flask(__name__)
CORS(app)


# ------------------------------------
# app routes for Meeting
# ------------------------------------
@app.route('/waza/meeting/', methods=['POST', 'GET'])
def meetings():
    if request.method == "POST":
        return BaseMeeting().addNewMeeting(request.form)
    else:
        return BaseMeeting().getAllMeetings()


@app.route('/waza/meeting/<int:mid>', methods=['DELETE', 'GET', 'PUT'])
def meetings_detail(mid):
    if request.method == 'GET':
        return BaseMeeting().getMeetingById(mid)
    elif request.method == 'DELETE':
        return BaseMeeting().deleteMeeting(mid)
    elif request.method == 'PUT':
        return BaseMeeting().updateMeeting(mid, request.form)
    else:
        return jsonify("Method Not Allowed"), 405


# ------------------------------------
# app routes for Room
# ------------------------------------

@app.route('/waza/room/', methods=['POST', 'GET'])
def room():
    connection = tbd_config.connection
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
    connection = tbd_config.connection
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
        # Meeting.put(connection, room["id"], roomtype_id, department_id, name, capacity)
        return {
                   "message": ("Room with id %s was updated" % (room["id"]))
               }, 200

    else:
        return room


# ------------------------------------
# app routes for Invitee
# ------------------------------------

@app.route('/waza/invitee/', methods=['POST', 'GET'])
def invitees():
    if request.method == "POST":
        return BaseInvitee().addNewInvitee(request.form)
    else:
        return BaseInvitee().getAllInvitees()


@app.route('/waza/invitee/<int:iid>', methods=['DELETE', 'GET', 'PUT'])
def invitees_detail(iid):
    if request.method == 'GET':
        return BaseInvitee().getInviteeById(iid)
    elif request.method == 'DELETE':
        return BaseInvitee().deleteInvitee(iid)
    elif request.method == 'PUT':
        return BaseInvitee().updateInvitee(iid, request.form)
    else:
        return jsonify("Method Not Allowed"), 405

# ------------------------------------
# app routes for Users
# ------------------------------------
@app.route('waza/user/', methods=['POST', 'GET'])
def users():
    if request.method == "POST":
        return BaseUser().addNewUser(request.form)
    else:
        return BaseUser().getAllUsers()

@app.route('waza/user/<int:uid>', methods=['DELETE', 'GET', 'PUT'])
def users_detail(uid):
    if request.method == "GET":
        return BaseUser().getUserById(uid)
    elif request.method == "DELETE":
        return BaseUser().deleteUser(uid)
    elif request.method == "PUT":
        return BaseUser().updateUser(uid, request.form)
    else:
        return jsonify("Method Not Allowed"),405


if __name__ == '__main__':
    app.run()
