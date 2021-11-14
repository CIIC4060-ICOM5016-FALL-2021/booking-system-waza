from model.user import UserDAO
from flask import jsonify


class BaseUser:
    def getAllUsers(self):
        dao = UserDAO()
        users = dao.getAllUsers()
        return jsonify(users), 200

    def getUserById(self, uid):
        dao = UserDAO()
        user = dao.getUserById(uid)
        if not user:
            return jsonify("Not Found"), 404
        else:
            return jsonify(user), 200

    def addNewUser(self, data):
        dao = UserDAO()
        
        role_id = data.get('role_id', '')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        email = data.get('email', '')
        phone = data.get('phone', '')
        
        uid = dao.addNewUser(role_id, first_name, last_name, email, phone)
        return self.getUserById(uid)

    def updateUser(self, uid, data):
        dao = UserDAO()
        
        role_id = data.get('role_id', '')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        email = data.get('email', '')
        phone = data.get('phone', '')
        
        result = dao.updateUser(uid, role_id, first_name, last_name, email, phone)
        return self.getUserById(uid)

    def deleteUser(self, uid):
        dao = UserDAO()
        result = dao.deleteUser(uid)
        if result:
            return jsonify("DELETED"), 200
        return jsonify("NOT FOUND"), 404


