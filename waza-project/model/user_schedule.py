from config.dbconfig import pg_config
import psycopg2
import psycopg2.extras
from datetime import datetime


class UserScheduleDAO:
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

    def addNewUserSchedule(self, user_id, start_at, end_at):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            time_now = datetime.now()
            qry = "INSERT INTO userschedule (user_id, start_at, end_at, created_at) values (%s, %s, %s, %s) RETURNING id;"
            cur.execute(qry, (user_id, start_at, end_at, time_now,))
            self.conn.commit()
            record_id = cur.fetchone()['id']
            cur.close()
            return record_id

    def getUserScheduleById(self, usid):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            qry = "SELECT * FROM userschedule WHERE id = %s;"
            cur.execute(qry, (usid,))
            record = cur.fetchone()
            cur.close()
            return record

    def getAllUserSchedule(self):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            qry = "SELECT * FROM userschedule;"
            cur.execute(qry)
            records = cur.fetchall()
            cur.close()
            return records

    def deleteUserSchedule(self, usid):
        with self.conn.cursor() as cur:
            qry = "DELETE FROM userschedule WHERE id = %s;"
            cur.execute(qry, (usid,))
            self.conn.commit()
            cur.close()
            return True

    def updateUserSchedule(self, usid, user_id, start_at, end_at):
        with self.conn.cursor() as cur:
            qry = "Update userschedule SET user_id = (%s), start_at = (%s), end_at = (%s) WHERE id = (%s);"
            cur.execute(qry, (user_id, start_at, end_at, usid,))
            self.conn.commit()
            cur.close()
            return True

    def checkUserScheduleSlot(self, usid, user_id, start_at, end_at):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            qry = """ 
                WITH user_schedule AS (
                    SELECT
                    us.user_id
                    ,us.start_at
                    ,us.end_at
                    ,us.created_at
                    FROM userschedule us"""
            qry += """  WHERE us.id <> %s  """ if usid is not None else "" #exclude current user schedule (used for updates)
            qry += """      
                    UNION
                    SELECT
                    i.user_id
                    ,m.start_at
                    ,m.end_at
                    ,m.created_at
                    FROM invitee i
                    LEFT JOIN meeting m on m.id = i.meeting_id    
                )
                
                SELECT * FROM user_schedule WHERE user_id = %s AND start_at < %s AND end_at > %s
            """
            fields = (usid, user_id, end_at, start_at,) if usid is not None else (user_id, end_at, start_at,)
            cur.execute(qry, fields)
            records = cur.fetchall()
            cur.close()
            return records


def allDayAvailability(self, user_id):
    with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        qry = """ 
               WITH user_schedule AS (
           SELECT
           us.user_id
           ,us.start_at
           ,us.end_at
           ,us.created_at
           FROM userschedule us
           UNION
           SELECT
           i.user_id
           ,m.start_at
           ,m.end_at
           ,m.created_at
           FROM invitee i
           LEFT JOIN meeting m on m.id = i.meeting_id
           )

           SELECT * FROM user_schedule us
           WHERE us.user_id = %s AND us.start_at BETWEEN current_date and (current_date + INTERVAL '1day')
           """
        fields = (user_id,)
        cur.execute(qry, fields)
        records = cur.fetchall()
        cur.close()
        return records
