from model.room import RoomDAO
from flask import jsonify


class BaseRoom:
    def getAllRooms(self):
        dao = RoomDAO()
        rooms = dao.getAllRooms()
        return jsonify(rooms), 200

    def getRoomById(self, rid):
        dao = RoomDAO()
        room = dao.getRoomById(rid)
        if not room:
            return jsonify("Not Found"), 404
        else:
            return jsonify(room), 200

    def addNewRoom(self, data):
        dao = RoomDAO()
        roomtype_id = data.get('roomtype_id', '')
        department_id = data.get('department_id', '')
        name = data.get('name', '')
        capacity = data.get('capacity', '')
        
        rid = dao.addNewRoom(roomtype_id, department_id, name, capacity)
        return self.getRoomById(rid)

    def updateRoom(self, rid, data):
        dao = RoomDAO()
        
        roomtype_id = data.get('roomtype_id', '')
        department_id = data.get('department_id', '')
        name = data.get('name', '')
        capacity = data.get('capacity', '')
        
        result = dao.updateRoom(rid, roomtype_id, department_id, name, capacity)
        return self.getRoomById(rid)

    def deleteRoom(self, rid):
        dao = RoomDAO()
        result = dao.deleteRoom(rid)
        if result:
            return jsonify("DELETED"), 200
        return jsonify("NOT FOUND"), 404

    def getRoomtUser(self, arguments):
        dao = RoomDAO()
        start_at = arguments.get('start_at', '')
        end_at = arguments.get('end_at', '')
        room_appointment = dao.getRoomtUser(start_at,end_at)
        if not room_appointment:
            return jsonify("Not Found"), 404
        else:
            return jsonify(room_appointment), 200

    def getAvailableRoom(self, arguments):
        dao = RoomDAO()
        start_at = arguments.get('start_at', '')
        end_at = arguments.get('end_at', '')
        room_availableRoom = dao.getAvailableRoom(start_at,end_at)
        if not room_availableRoom:
            return jsonify("Not Found"), 404
        else:
            return jsonify(room_availableRoom), 200


