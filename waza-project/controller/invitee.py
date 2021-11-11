from model.invitee import InviteeDAO
from flask import jsonify


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
        user_id = data.get('user_id', '')
        meeting_id = data.get('meeting_id', '')
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


