from flask_cors import CORS
from flask import Flask, request, jsonify, abort
from controller.meeting import BaseMeeting
from controller.invitee import BaseInvitee
from controller.user import BaseUser
from controller.statistics_user import BaseStatisticsUser
from controller.statistics_global import BaseStatisticsGlobal
from controller.room_schedule import BaseRoomSchedule
from controller.user_schedule import BaseUserSchedule
from controller.room import BaseRoom


app = Flask(__name__)
CORS(app)


# ------------------------------------
# app routes for Meeting
# ------------------------------------
@app.route('/waza/meeting/', methods=['POST', 'GET'])
def meetings():
    if request.method == "POST":
        return BaseMeeting().addNewMeeting(request.form, request.args)
    else:
        return BaseMeeting().getAllMeetings(request.args)


@app.route('/waza/meeting/<int:mid>', methods=['DELETE', 'GET', 'PUT'])
def meetings_detail(mid):
    if request.method == 'GET':
        return BaseMeeting().getMeetingById(mid, request.args)
    elif request.method == 'DELETE':
        return BaseMeeting().deleteMeeting(mid, request.args)
    elif request.method == 'PUT':
        return BaseMeeting().updateMeeting(mid, request.form, request.args)
    else:
        return jsonify("Method Not Allowed"), 405


# ------------------------------------
# app routes for Room
# ------------------------------------

@app.route('/waza/room/', methods=['POST', 'GET'])
def room():
    if request.method == "POST":
        return BaseRoom().addNewRoom(request.form)
    else:
        return BaseRoom().getAllRooms()


@app.route('/waza/room/<int:room_id>', methods=['DELETE', 'GET', 'PUT'])
def room_detail(room_id):
    if request.method == "GET":
        return BaseRoom().getRoomById(room_id)
    elif request.method == "DELETE":
        return BaseRoom().deleteRoom(room_id)
    elif request.method == "PUT":
        return BaseRoom().updateRoom(room_id, request.form)
    else:
        return jsonify("Method Not Allowed"), 405


# ------------------------------------
# app routes for RoomSchedule
# ------------------------------------

@app.route('/waza/roomschedule/', methods=['POST', 'GET'])
def roomschedule():
    if request.method == "POST":
        return BaseRoomSchedule().addNewRoomSchedule(request.form, request.args)
    else:
        return BaseRoomSchedule().getAllRoomSchedule()

@app.route('/waza/roomschedule/<int:rsid>', methods=['DELETE', 'GET', 'PUT'])
def roomschedule_detail(rsid):
    if request.method == 'GET':
        return BaseRoomSchedule().getRoomScheduleById(rsid)
    elif request.method == 'DELETE':
        return BaseRoomSchedule().deleteRoomSchedule(rsid)
    elif request.method == 'PUT':
        return BaseRoomSchedule().updateRoomSchedule(rsid, request.form, request.args)
    else:
        return jsonify("Method Not Allowed"), 405


# ------------------------------------
# app routes for UserSchedule
# ------------------------------------

@app.route('/waza/userschedule/', methods=['POST', 'GET'])
def userschedule():
    if request.method == "POST":
        return BaseUserSchedule().addNewUserSchedule(request.form)
    else:
        return BaseUserSchedule().getAllUserSchedule()

@app.route('/waza/userschedule/<int:usid>', methods=['DELETE', 'GET', 'PUT'])
def userschedule_detail(usid):
    if request.method == 'GET':
        return BaseUserSchedule().getUserScheduleById(usid)
    elif request.method == 'DELETE':
        return BaseUserSchedule().deleteUserSchedule(usid)
    elif request.method == 'PUT':
        return BaseUserSchedule().updateUserSchedule(usid, request.form)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/waza/user/availability/<int:uid>', methods=['GET'])
def user_availability(uid):
    return BaseUserSchedule().getUserAvailabilityById(uid)

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
@app.route('/waza/user/', methods=['POST', 'GET'])
def users():
    if request.method == "POST":
        return BaseUser().addNewUser(request.form)
    else:
        return BaseUser().getAllUsers()


@app.route('/waza/user/<int:uid>', methods=['DELETE', 'GET', 'PUT'])
def users_detail(uid):
    if request.method == "GET":
        return BaseUser().getUserById(uid)
    elif request.method == "DELETE":
        return BaseUser().deleteUser(uid)
    elif request.method == "PUT":
        return BaseUser().updateUser(uid, request.form)
    else:
        return jsonify("Method Not Allowed"),405




# ------------------------------------
# app routes for User Statistics
# ------------------------------------
@app.route('/waza/statistics/user/most-used-room', methods=['GET'])
def statistics_user_most_used_room():
    return BaseStatisticsUser().getMostUsedRoomWithUsers(request.args)

@app.route('/waza/statistics/user/most-booked', methods=['GET'])
def statistics_user_most_booked():
    return BaseStatisticsUser().getMostBookedPeerUsers(request.args)

# ------------------------------------
# app routes for Global Statistics
# ------------------------------------
@app.route('/waza/statistics/global/busiest-hours', methods=['GET'])
def statistics_global_busiest_hours():
    return BaseStatisticsGlobal().getBusiestHours()

@app.route('/waza/statistics/global/most-booked-users', methods=['GET'])
def statistics_global_most_booked_users():
    return BaseStatisticsGlobal().getMostBookedUsers()

@app.route('/waza/statistics/global/most-booked-rooms', methods=['GET'])
def statistics_global_most_booked_rooms():
    return BaseStatisticsGlobal().getMostBookedRooms()


if __name__ == '__main__':
    app.run()
