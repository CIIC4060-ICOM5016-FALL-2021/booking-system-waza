from model.statistics_user import StatisticsUserDAO
from flask import jsonify


class BaseStatisticsUser:
    def getMostUsedRoomWithUsers(self):
        dao = StatisticsUserDAO()
        result = dao.getMostUsedRoomWithUsers()
        return jsonify(result), 200

    def getMostBookedUsers(self):
        dao = StatisticsUserDAO()
        result = dao.getMostBookedUsers()
        return jsonify(result), 200
