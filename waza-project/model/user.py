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

    def addNewUser(self, user_id, first_name, last_name, email, phone, schedule_id, meeting_id):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            #time_now = datetime.now()
            qry = "INSERT INTO users (id, first_name, last_name, email, phone, created_at, schedule_id, meeting_id) VALUES (%s, %s, %s, %s, %s, now(), %s, %s) RETURNING id"
            cur.execute(qry, (user_id, first_name, last_name, email, phone, schedule_id, meeting_id,))
            self.conn.commit()
            record_id = cur.fetchone()['id']
            cur.close()
            return record_id

    def getUserById(self, user_id):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            qry = "SELECT * FROM users WHERE id = %s;"
            cur.execute(qry, (user_id,))
            record = cur.fetchone()
            cur.close()
            return record

    def getAllUsers(self):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            qry = "SELECT * FROM users;"
            cur.execute(qry)
            records = cur.fetchall()
            cur.close()
            return records

    def deleteUser(self, mid):
        with self.conn.cursor() as cur:
            qry = "DELETE FROM users WHERE id = %s;"
            cur.execute(qry, (mid,))
            self.conn.commit()
            cur.close()
            return True

    def updateUser(self, user_id, first_name, last_name, email, phone, schedule_id, meeting_id):
        with self.conn.cursor() as cur:
            qry = "Update User SET user_id = (%s), first_name = (%s), last_name = (%s), email = (%s), phone = (%s), scehdule_id = (%s), meeting_id = (%s) WHERE id = (%s);"
            cur.execute(qry, (user_id, first_name, last_name, email, phone, schedule_id, meeting_id, ))
            self.conn.commit()
            cur.close()
            return True
