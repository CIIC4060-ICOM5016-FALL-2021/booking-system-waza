from flask import Flask, request, jsonify, abort
import config
from model.meeting import Meeting
from model.invitee import Invitee

app = Flask(__name__)


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


@app.route('/waza/invitee/', methods=['POST', 'GET'])
def invitees():
    connection = config.connection
    if request.method == "POST":
        user_id = request.form.get('user_id', '')
        meeting_id = request.form.get('meeting_id', '')
        invite_id = Invitee.post(connection, user_id, meeting_id)
        return {
            "message": ("Invitee with id %s was inserted" % (invite_id))
        }, 200
    else:
        response = jsonify(Invitee.get_all(connection))
        response.status_code = 200
        return response


@app.route('/waza/invitee/<int:invitee_id>', methods=['DELETE', 'GET', 'PUT'])
def invitees_detail(invitee_id):
    connection = config.connection
    invite = Invitee.get_first(connection, invitee_id)
    if not invite:
        abort(404)

    if request.method == 'DELETE':
        Invitee.delete(connection, invite["id"])
        return {
            "message": ("Invitee with id %s was removed" % (invite["id"]))
        }, 200

    elif request.method == 'PUT':
        user_id = request.form.get('user_id', '')
        meeting_id = request.form.get('meeting_id', '')
        Invitee.put(connection, invite["id"], user_id, meeting_id)
        return {
            "message": ("Invitee with id %s was updated" % (invite["id"]))
        }, 200

    else:
        return invite


if __name__ == '__main__':
    app.run()
