from model.invitee import InviteeDAO
from model.room import RoomDAO
from model.meeting import MeetingDAO
from flask import jsonify, json
import datetime


class BaseInvitee:
    def getAllInvitees(self):
        dao = InviteeDAO()
        invitees = dao.getAllInvitees()
        return jsonify(invitees), 200


    def getInviteeById(self, iid):
        dao = InviteeDAO()
        invitee = dao.getInviteeById(iid)
        if not invitee:
            return jsonify("Not Found"), 404
        else:
            return jsonify(invitee), 200


    def addNewInvitee(self, data):
        dao = InviteeDAO()
        rdao = RoomDAO()
        user_id = data.get('user_id', '')
        meeting_id = data.get('meeting_id', '')
        # check if it has space left
        room_capacity_available = rdao.getRoomCapacityAvailableByMeeting(meeting_id)
        if room_capacity_available['available_capacity'] <= 0:
            return jsonify("This room has reached full capacity."), 400
        # check if is available
        unavailable = dao.checkInviteeUnavailability(user_id, meeting_id)
        if unavailable:
            return jsonify("The user already has a meeting at this time."), 400
        iid = dao.addNewInvitee(user_id, meeting_id)
        return self.getInviteeById(iid)


    def updateInvitee(self, iid, data):
        dao = InviteeDAO()
        user_id = data.get('user_id', '')
        meeting_id = data.get('meeting_id', '')
        result = dao.updateInvitee(iid, user_id, meeting_id)
        return self.getInviteeById(iid)


    def deleteInvitee(self, iid):
        dao = InviteeDAO()
        result = dao.deleteInvitee(iid)
        if iid:
            return jsonify("DELETED"), 200
        return jsonify("NOT FOUND"), 404

    def addMeetingWithInvitees(self, data):
        dao = InviteeDAO()
        mdao = MeetingDAO()
        rdao = RoomDAO()
        created_by = data.get('created_by', '')
        room_id = data.get('room_id', '')
        start_at = data.get('start_at', '')
        end_at = data.get('end_at', '')
        users = data.get('users', '')
        name = data.get('name', '')
        description = data.get('description', '')
        user_list = json.loads(users)
        try:
            # validate date
            start_at = datetime.datetime.strptime(start_at, "%Y-%m-%d %H:%M:%S")
            end_at = datetime.datetime.strptime(end_at, "%Y-%m-%d %H:%M:%S")
        except ValueError as e:
            return jsonify("Invalid datetime. Please provide a valid datetime for start_at and end_at in the form: YYYY-MM-DD HH:MM:SS."), 400
        if start_at > end_at:
            return jsonify("A meeting cannot have a start_at that is greater than its end_at."), 400

        meeting = mdao.addNewMeeting(created_by, room_id, start_at, end_at, name, description)
        room_capacity_available = rdao.getRoomCapacityAvailableByMeeting(meeting)

        if room_capacity_available['available_capacity'] <= 0 or room_capacity_available['available_capacity'] < len(users):
            return jsonify("This room has reached full capacity or will overflow."), 400

        unavailable_users = ''
        for user in user_list:
            unavailable = dao.checkInviteeUnavailability(user, meeting)
            if unavailable:
                unavailable_users += str(user) + ', '
                continue
            dao.addNewInvitee(user, meeting)

        if unavailable_users:
            return jsonify("The following user(s) could not be added to the meeting " + unavailable_users), 202

        return jsonify(mdao.getMeetingById(meeting)), 200

    def getMeetingWithInviteesDetail(self, mid, arguments):
        dao = InviteeDAO()
        invitee = dao.getMeetingWithInviteesDetail(mid)
        if not invitee:
            return jsonify("Not Found"), 404
        else:
            return jsonify(invitee), 200

