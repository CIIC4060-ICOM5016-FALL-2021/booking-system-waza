from config.dbconfig import pg_config
import psycopg2
import psycopg2.extras
from datetime import datetime
from psycopg2 import errors

'''ASS'''
#HOLE
class UserDAO:
    def __init__(self):
        self.conn = psycopg2.connect(host=pg_config['host'],
                                     port=pg_config['port'],
                                     dbname=pg_config['dbname'],
                                     user=pg_config['user'],
                                     password=pg_config['password'],
                                     )

    def addNewUser(self, created_at, first_name, last_name, email, phone):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            time_now = datetime.now()
            qry = "INSERT INTO User (created_by, room_id, start_at, end_at, created_at) VALUES (%s, %s, %s, %s, %s) RETURNING id"
            cur.execute(qry, (created_by, room_id, start_at, end_at, time_now,))
            self.conn.commit()
            record_id = cur.fetchone()['id']
            cur.close()
            return record_id

    def getUserById(self, user_id):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            qry = "SELECT * FROM User WHERE id = %s;"
            cur.execute(qry, (user_id,))
            record = cur.fetchone()
            cur.close()
            return record

    def getAllUsers(self):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            qry = "SELECT * FROM User;"
            cur.execute(qry)
            records = cur.fetchall()
            cur.close()
            return records

    def deleteUser(self, mid):
        with self.conn.cursor() as cur:
            qry = "DELETE FROM User WHERE id = %s;"
            cur.execute(qry, (mid,))
            self.conn.commit()
            cur.close()
            return True

    def updateUser(self, mid, created_at, first_name, last_name, email, phone):
        with self.conn.cursor() as cur:
            qry = "Update User SET created_at = (%s), first_name = (%s), last_name = (%s), WHERE id = (%s);"
            cur.execute(qry, (created_by, start_at, end_at, mid,))
            self.conn.commit()
            cur.close()
            return True
