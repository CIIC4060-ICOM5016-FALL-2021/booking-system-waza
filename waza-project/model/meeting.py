#from config.dbconfig import pg_config
import psycopg2
import psycopg2.extras
from datetime import datetime
from psycopg2 import errors


class MeetingDAO:
    def __init__(self):
        pg_config = {
            'host': 'ec2-44-195-240-222.compute-1.amazonaws.com',
            'port': '5432',
            'dbname': 'd4t9n848bvcar7',
            'user': 'ohdxiligkvesze',
            'password': '8cd54a2a07d88668cb543bbaf0cfc45f523091779c47ca91f071d41798411507'
        }
        self.conn = psycopg2.connect(host=pg_config['host'],
                                     port=pg_config['port'],
                                     dbname=pg_config['dbname'],
                                     user=pg_config['user'],
                                     password=pg_config['password'],
                                     )

    def addNewMeeting(self, created_by, room_id, start_at, end_at):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            time_now = datetime.now()
            qry = "INSERT INTO Meeting (created_by, room_id, start_at, end_at, created_at) VALUES (%s, %s, %s, %s, %s) RETURNING id"
            cur.execute(qry, (created_by, room_id, start_at, end_at, time_now,))
            self.conn.commit()
            record_id = cur.fetchone()['id']
            cur.close()
            return record_id

    def getMeetingById(self, meeting_id):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            qry = "SELECT * FROM Meeting WHERE id = %s;"
            cur.execute(qry, (meeting_id,))
            record = cur.fetchone()
            cur.close()
            return record

    def getAllMeetings(self):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            qry = "SELECT * FROM Meeting;"
            cur.execute(qry)
            records = cur.fetchall()
            cur.close()
            return records

    def deleteMeeting(self, mid):
        with self.conn.cursor() as cur:
            qry = "DELETE FROM Meeting WHERE id = %s;"
            cur.execute(qry, (mid,))
            self.conn.commit()
            cur.close()
            return True

    def updateMeeting(self, mid, created_by, room_id, start_at, end_at):
        with self.conn.cursor() as cur:
            qry = "Update Meeting SET created_by = (%s), room_id = (%s), start_at = (%s), end_at = (%s) WHERE id = (%s);"
            cur.execute(qry, (created_by, room_id, start_at, end_at, mid,))
            self.conn.commit()
            cur.close()
            return True
