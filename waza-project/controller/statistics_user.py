from model.statistics_user import StatisticsUserDAO
from flask import jsonify


class BaseStatisticsUser:
    def getMostUsedRoomWithUsers(self, data):
        dao = StatisticsUserDAO()
        result = dao.getMostUsedRoomWithUsers(data['user_id'])
        return jsonify(result), 200

    def getMostBookedPeerUsers(self, data):
        dao = StatisticsUserDAO()
        result = dao.getMostBookedPeerUsers(data['user_id'])
        return jsonify(result), 200
