from model.invitee import InviteeDAO
from model.room import RoomDAO
from model.meeting import MeetingDAO
from flask import jsonify, json
import datetime

class UnavailableError(Exception):
    pass


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

    def addMoreInvitee(self, data, arguments):
        dao = InviteeDAO()
        mdao = MeetingDAO()
        rdao = RoomDAO()
        #users = dao.getUserIdFromAllInvitees().split("")
        host = data.get('host', '')
        room = data.get('room_id', '')
        start = data.get('start_at', '')
        end  = data.get('end_at', '')
        users = arguments.get('users', '')
        user_list = json.loads(users)

        try:
            # validate date
            start = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
            end = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
        except ValueError as e:
            return jsonify("Invalid datetime. Please provide a valid datetime for start_at and end_at in the form: YYYY-MM-DD HH:MM:SS."), 400
        if start > end:
            return jsonify("A meeting cannot have a start_at that is greater than its end_at."), 400

        meeting = mdao.addNewMeeting(host, room, start, end)
        room_capacity_available = rdao.getRoomCapacityAvailableByMeeting(meeting)

        if room_capacity_available['available_capacity'] <= 0 or room_capacity_available['available_capacity'] < len(users):
            return jsonify("This room has reached full capacity or will overflow."), 400

        try:
            for user in user_list:
                unavailable = dao.checkInviteeUnavailability(user, meeting)
                if unavailable:
                    raise UnavailableError
                dao.addNewInvitee(user, meeting)
        except UnavailableError:
            return jsonify("The user already has a meeting at this time."), 400

        finally:
            return jsonify("Meeting with users successfully created."), 200
