from model.room_schedule import RoomScheduleDAO
from flask import jsonify
import datetime


class BaseRoomSchedule:
    def getAllRoomSchedule(self):
        dao = RoomScheduleDAO()
        invitees = dao.getAllRoomSchedule()
        return jsonify(invitees), 200


    def getRoomScheduleById(self, rsid):
        dao = RoomScheduleDAO()
        invitee = dao.getRoomScheduleById(rsid)
        if not invitee:
            return jsonify("Not Found"), 404
        else:
            return jsonify(invitee), 200


    def addNewRoomSchedule(self, data):
        # TODO: validate user role
        dao = RoomScheduleDAO()
        room_id = data.get('room_id', '')
        start_at = data.get('start_at', '')
        end_at = data.get('end_at', '')
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
        return self.getRoomScheduleById(rsid)


    def updateRoomSchedule(self, rsid, data):
        # TODO: validate user role
        dao = RoomScheduleDAO()
        room_id = data.get('room_id', '')
        start_at = data.get('start_at', '')
        end_at = data.get('end_at', '')
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
        return self.getRoomScheduleById(rsid)


    def deleteRoomSchedule(self, rsid):
        dao = RoomScheduleDAO()
        result = dao.deleteRoomSchedule(rsid)
        if result:
            return jsonify("DELETED"), 200
        return jsonify("NOT FOUND"), 404

