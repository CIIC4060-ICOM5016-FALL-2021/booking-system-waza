from config.dbconfig import pg_config
import psycopg2
import psycopg2.extras
from datetime import datetime
from psycopg2 import errors


class UserDAO:
    def __init__(self):
        self.conn = psycopg2.connect(host=pg_config['host'],
                                     port=pg_config['port'],
                                     dbname=pg_config['dbname'],
                                     user=pg_config['user'],
                                     password=pg_config['password'],
                                     )

    def addNewUser(self, role_id, first_name, last_name, email, phone):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            time_now = datetime.now()
            qry = "INSERT INTO \"User\" (role_id, first_name, last_name, email, phone, created_at) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id"
            cur.execute(qry, (role_id, first_name, last_name, email, phone, time_now))
            self.conn.commit()
            record_id = cur.fetchone()['id']
            cur.close()
            return record_id

    def getUserById(self, user_id):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            qry = "SELECT * FROM \"User\" WHERE id = %s;"
            cur.execute(qry, (user_id,))
            record = cur.fetchone()
            cur.close()
            return record

    def getAllUsers(self):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            qry = "SELECT * FROM \"User\";"
            cur.execute(qry)
            records = cur.fetchall()
            cur.close()
            return records

    def deleteUser(self, mid):
        with self.conn.cursor() as cur:
            qry = "DELETE FROM \"User\" WHERE id = %s;"
            cur.execute(qry, (mid,))
            self.conn.commit()
            cur.close()
            return True

    def updateUser(self, role_id, first_name, last_name, email, phone,):
        with self.conn.cursor() as cur:
            qry = "Update User SET role_id = (%s), first_name = (%s), last_name = (%s), email = (%s), phone = (%s) WHERE id = (%s);"
            cur.execute(qry, (user_id, first_name, last_name, email, phone, ))
            self.conn.commit()
            cur.close()
            return True
