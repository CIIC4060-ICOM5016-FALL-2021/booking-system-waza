from model.statistics_global import StatisticsGlobalDAO
from flask import jsonify


class BaseStatisticsGlobal:
    def getBusiestHours(self):
        dao = StatisticsGlobalDAO()
        result = dao.getBusiestHours()
        return jsonify(result), 200

    def getMostBookedUsers(self):
        dao = StatisticsGlobalDAO()
        result = dao.getMostBookedUsers()
        return jsonify(result), 200

    def getMostBookedRooms(self):
        dao = StatisticsGlobalDAO()
        result = dao.getMostBookedRooms()
        return jsonify(result), 200