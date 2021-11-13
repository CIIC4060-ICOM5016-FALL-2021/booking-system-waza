from model.user_schedule import UserScheduleDAO
from flask import jsonify
import datetime


class BaseUserSchedule:
    def getAllUserSchedule(self):
        dao = UserScheduleDAO()
        invitees = dao.getAllUserSchedule()
        return jsonify(invitees), 200


    def getUserScheduleById(self, rsid):
        dao = UserScheduleDAO()
        invitee = dao.getUserScheduleById(rsid)
        if not invitee:
            return jsonify("Not Found"), 404
        else:
            return jsonify(invitee), 200


    def addNewUserSchedule(self, data):
        # TODO: validate user role
        dao = UserScheduleDAO()
        user_id = data.get('user_id', '')
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
        unavailable = dao.checkUserScheduleSlot(user_id, start_at, end_at)
        if unavailable:
            return jsonify("This time slot is already reserved."), 400
        rsid = dao.addNewUserSchedule(user_id, start_at, end_at)
        return self.getUserScheduleById(rsid)


    def updateUserSchedule(self, rsid, data):
        # TODO: validate user role
        dao = UserScheduleDAO()
        user_id = data.get('user_id', '')
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
        unavailable = dao.checkUserScheduleSlot(user_id, start_at, end_at)
        if unavailable:
            return jsonify("This time slot is already reserved."), 400
        result = dao.updateUserSchedule(rsid, user_id, start_at, end_at)
        return self.getUserScheduleById(rsid)


    def deleteUserSchedule(self, rsid):
        dao = UserScheduleDAO()
        result = dao.deleteUserSchedule(rsid)
        if result:
            return jsonify("DELETED"), 200
        return jsonify("NOT FOUND"), 404

