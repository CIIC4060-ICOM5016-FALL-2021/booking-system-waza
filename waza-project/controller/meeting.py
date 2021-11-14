from model.meeting import MeetingDAO
from model.invitee import InviteeDAO
from model.user import UserDAO
from flask import jsonify
import datetime


class BaseMeeting:
    def getAllMeetings(self, arguments):
        dao = MeetingDAO()
        udao = UserDAO()
        user_id = arguments.get('user_id', '')
        user = udao.getUserById(user_id)

        if user['role_id'] not in range(1, 4):
            return jsonify("You do not have enough permissions for this operation."), 403
        
        meetings = dao.getAllMeetings()
        return jsonify(meetings), 200

    def getMeetingById(self, mid, arguments):
        dao = MeetingDAO()
        udao = UserDAO()
        user_id = arguments.get('user_id', '')
        user = udao.getUserById(user_id)

        if user['role_id'] not in range(1, 4):
            return jsonify("You do not have enough permissions for this operation."), 403
        
        meeting = dao.getMeetingById(mid)
        if not meeting:
            return jsonify("Not Found"), 404
        else:
            return jsonify(meeting), 200

    def addNewMeeting(self, data, arguments):
        dao = MeetingDAO()
        udao = UserDAO()
        created_by = data.get('created_by', '')
        room_id = data.get('room_id', '')
        start_at = data.get('start_at', '')
        end_at = data.get('end_at', '')
        user_id = arguments.get('user_id', '')
        user = udao.getUserById(user_id)

        if user['role_id'] not in range(1, 4):
            return jsonify("You do not have enough permissions for this operation."), 403
        
        try:
            # validate date
            start_at = datetime.datetime.strptime(start_at, "%Y-%m-%d %H:%M:%S")
            end_at = datetime.datetime.strptime(end_at, "%Y-%m-%d %H:%M:%S")
        except ValueError as e:
            return jsonify("Invalid datetime. Please provide a valid datetime for start_at and end_at in the form: YYYY-MM-DD HH:MM:SS."), 400
        if start_at > end_at:
            return jsonify("A meeting cannot have a start_at that is greater than its end_at."), 400
        mid = dao.addNewMeeting(created_by, room_id, start_at, end_at)
        return self.getMeetingById(mid)

    def updateMeeting(self, mid, data, arguments):
        dao = MeetingDAO()
        udao = UserDAO()
        created_by = data.get('created_by', '')
        room_id = data.get('room_id', '')
        start_at = data.get('start_at', '')
        end_at = data.get('end_at', '')
        user_id = arguments.get('user_id', '')
        user = udao.getUserById(user_id)

        if user['role_id'] not in range(1, 4):
            return jsonify("You do not have enough permissions for this operation."), 403
        
        try:
            # validate date
            start_at = datetime.datetime.strptime(start_at, "%Y-%m-%d %H:%M:%S")
            end_at = datetime.datetime.strptime(end_at, "%Y-%m-%d %H:%M:%S")
        except ValueError as e:
            return jsonify("Invalid datetime. Please provide a valid datetime for start_at and end_at in the form: YYYY-MM-DD HH:MM:SS."), 400
        result = dao.updateMeeting(mid, created_by, room_id, start_at, end_at)
        return self.getMeetingById(mid)

    def deleteMeeting(self, mid, arguments):
        idao = InviteeDAO()
        udao = UserDAO()

        if idao.getInviteeByMeetingId(mid):
            return jsonify("NOT ALLOWED. You need to delete any invitees with meeting_id = %s." % mid), 405

        dao = MeetingDAO()
        user_id = arguments.get('user_id', '')
        user = udao.getUserById(user_id)

        if user['role_id'] not in range(1, 4):
            return jsonify("You do not have enough permissions for this operation."), 403
        
        result = dao.deleteMeeting(mid)
        if result:
            return jsonify("DELETED"), 200
        return jsonify("NOT FOUND"), 404


