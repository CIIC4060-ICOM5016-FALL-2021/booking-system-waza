from model.user import UserDAO
from flask import jsonify



class BaseUser:
    def getAllUsers(self):
        dao = UserDAO()
        users = dao.getAllUsers()
        return jsonify(users), 200

    def getUserById(self, mid):
        dao = UserDAO()
        user = dao.getUserById(mid)
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
        
        mid = dao.addNewUser(role_id, first_name, last_name, email, phone)
        return self.getUserById(mid)

    def updateUser(self, mid, data):
        dao = UserDAO()
        
        role_id = data.get('role_id', '')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        email = data.get('email', '')
        phone = data.get('phone', '')
        
        result = dao.updateUser(role_id, first_name, last_name, email, phone)
        return self.getUserById(result)

    def deleteUser(self, mid):
        dao = UserDAO()
        result = dao.deleteUser(mid)
        if result:
            return jsonify("DELETED"), 200
        return jsonify("NOT FOUND"), 404


