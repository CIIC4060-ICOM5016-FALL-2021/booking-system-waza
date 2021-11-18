from model.room_schedule import RoomScheduleDAO
from model.user import UserDAO
from flask import jsonify
import datetime


class BaseRoomSchedule:
    def getAllRoomSchedule(self, arguments):
        dao = RoomScheduleDAO()
        udao = UserDAO()
        user_id = arguments.get('user_id', '')
        user = udao.getUserById(user_id)

        if user['role_id'] not in range(1, 4):
            return jsonify("You do not have enough permissions for this operation."), 403

        invitees = dao.getAllRoomSchedule()
        return jsonify(invitees), 200


    def getRoomScheduleById(self, rsid, arguments):
        dao = RoomScheduleDAO()
        udao = UserDAO()
        user_id = arguments.get('user_id', '')
        user = udao.getUserById(user_id)

        if user['role_id'] not in range(1, 4):
            return jsonify("You do not have enough permissions for this operation."), 403


        invitee = dao.getRoomScheduleById(rsid)
        if not invitee:
            return jsonify("Not Found"), 404
        else:
            return jsonify(invitee), 200


    def addNewRoomSchedule(self, data, arguments):
        dao = RoomScheduleDAO()
        udao = UserDAO()
        room_id = data.get('room_id', '')
        start_at = data.get('start_at', '')
        end_at = data.get('end_at', '')
        user_id = arguments.get('user_id', '')
        # validate user role
        user = udao.getUserById(user_id)
        if user['role_id'] != 1:
            return jsonify("You don't have enough permissions for this operation."), 401
        # validate date
        try:
            start_at = datetime.datetime.strptime(start_at, "%Y-%m-%d %H:%M:%S")
            end_at = datetime.datetime.strptime(end_at, "%Y-%m-%d %H:%M:%S")
        except ValueError as e:
            return jsonify("Invalid datetime. Please provide a valid datetime for start_at and end_at in the form: YYYY-MM-DD HH:MM:SS."), 400
        # validate ranges
        if start_at > end_at:
            return jsonify("A meeting cannot have a start_at that is greater than its end_at."), 400
        # check if there are other schedules at this time
        unavailable = dao.checkRoomScheduleSlot(None, room_id, start_at, end_at)
        if unavailable:
            return jsonify("This time slot is already reserved."), 400
        rsid = dao.addNewRoomSchedule(room_id, start_at, end_at)
        return self.getRoomScheduleById(rsid, arguments)


    def updateRoomSchedule(self, rsid, data, arguments):
        dao = RoomScheduleDAO()
        udao = UserDAO()
        room_id = data.get('room_id', '')
        start_at = data.get('start_at', '')
        end_at = data.get('end_at', '')
        user_id = arguments.get('user_id', '')
        # validate user role
        user = udao.getUserById(user_id)
        if user['role_id'] != 1:
            return jsonify("You don't have enough permissions for this operation."), 401
        # validate date
        try:
            start_at = datetime.datetime.strptime(start_at, "%Y-%m-%d %H:%M:%S")
            end_at = datetime.datetime.strptime(end_at, "%Y-%m-%d %H:%M:%S")
        except ValueError as e:
            return jsonify("Invalid datetime. Please provide a valid datetime for start_at and end_at in the form: YYYY-MM-DD HH:MM:SS."), 400
        # validate ranges
        if start_at > end_at:
            return jsonify("A meeting cannot have a start_at that is greater than its end_at."), 400
        # check if there are other schedules at this time
        unavailable = dao.checkRoomScheduleSlot(rsid, room_id, start_at, end_at)
        if unavailable:
            return jsonify("This time slot is already reserved."), 400
        result = dao.updateRoomSchedule(rsid, room_id, start_at, end_at)
        return self.getRoomScheduleById(rsid, arguments)


    def deleteRoomSchedule(self, rsid, arguments):
        dao = RoomScheduleDAO()
        udao = UserDAO()
        user_id = arguments.get('user_id', '')
        user = udao.getUserById(user_id)

        if user['role_id'] not in range(1, 4):
            return jsonify("You do not have enough permissions for this operation."), 403

        result = dao.deleteRoomSchedule(rsid)
        if result:
            return jsonify("DELETED"), 200
        return jsonify("NOT FOUND"), 404

    def getRoomAvailabilityById(self, rid, arguments):
        dao = RoomScheduleDAO()
        udao = UserDAO()
        user_id = arguments.get('user_id', '')
        user = udao.getUserById(user_id)

        if user['role_id'] not in range(1, 4):
            return jsonify("You do not have enough permissions for this operation."), 403

        result = dao.allDayAvailability(rid)
        if result:
            return jsonify(result), 200
        return jsonify("NOT FOUND"), 404

