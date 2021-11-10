from model.meeting import MeetingDAO
from model.invitee import InviteeDAO
from flask import jsonify


class BaseMeeting:
    def getAllMeetings(self):
        dao = MeetingDAO()
        meetings = dao.getAllMeetings()
        return jsonify(meetings), 200

    def getMeetingById(self, mid):
        dao = MeetingDAO()
        meeting = dao.getMeetingById(mid)
        if not meeting:
            return jsonify("Not Found"), 404
        else:
            return jsonify(meeting), 200

    def addNewMeeting(self, data):
        dao = MeetingDAO()
        created_by = data.get('created_by', '')
        room_id = data.get('room_id', '')
        start_at = data.get('start_at', '')
        end_at = data.get('end_at', '')
        mid = dao.addNewMeeting(created_by, room_id, start_at, end_at)
        return self.getMeetingById(mid)

    def updateMeeting(self, mid, data):
        dao = MeetingDAO()
        created_by = data.get('created_by', '')
        room_id = data.get('room_id', '')
        start_at = data.get('start_at', '')
        end_at = data.get('end_at', '')
        result = dao.updateMeeting(mid, created_by, room_id, start_at, end_at)
        return self.getMeetingById(mid)

    def deleteMeeting(self, mid):
        idao = InviteeDAO()
        if idao.getInviteeByMeetingId(mid):
            return jsonify("NOT ALLOWED. You need to delete any invitees with meeting_id = %s." % mid), 405

        dao = MeetingDAO()
        result = dao.deleteMeeting(mid)
        if result:
            return jsonify("DELETED"), 200
        return jsonify("NOT FOUND"), 404


