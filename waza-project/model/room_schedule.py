from config.dbconfig import pg_config
import psycopg2
import psycopg2.extras
from datetime import datetime


class RoomScheduleDAO:
    def __init__(self):
        self.conn = psycopg2.connect(host=pg_config['host'],
                                     port=pg_config['port'],
                                     dbname=pg_config['dbname'],
                                     user=pg_config['user'],
                                     password=pg_config['password'],
                                     )

    def addNewRoomSchedule(self, room_id, start_at, end_at):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            time_now = datetime.now()
            qry = "INSERT INTO roomschedule (room_id, start_at, end_at, created_at) values (%s, %s, %s, %s) RETURNING id;"
            cur.execute(qry, (room_id, start_at, end_at, time_now,))
            self.conn.commit()
            record_id = cur.fetchone()['id']
            cur.close()
            return record_id

    def getRoomScheduleById(self, rsid):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            qry = "SELECT * FROM roomschedule WHERE id = %s;"
            cur.execute(qry, (rsid,))
            record = cur.fetchone()
            cur.close()
            return record

    def getAllRoomSchedule(self):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            qry = "SELECT * FROM roomschedule;"
            cur.execute(qry)
            records = cur.fetchall()
            cur.close()
            return records

    def deleteRoomSchedule(self, rsid):
        with self.conn.cursor() as cur:
            qry = "DELETE FROM roomschedule WHERE id = %s;"
            cur.execute(qry, (rsid,))
            self.conn.commit()
            cur.close()
            return True

    def updateRoomSchedule(self, rsid, room_id, start_at, end_at):
        with self.conn.cursor() as cur:
            qry = "Update roomschedule SET room_id = (%s), start_at = (%s), end_at = (%s) WHERE id = (%s);"
            cur.execute(qry, (room_id, start_at, end_at, rsid,))
            self.conn.commit()
            cur.close()
            return True

    def checkRoomScheduleSlot(self, room_id, start_at, end_at):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            qry = """ 
                WITH room_schedule AS (
                    SELECT
                    rs.room_id
                    ,rs.start_at
                    ,rs.end_at
                    ,rs.created_at
                    FROM roomschedule rs
                    UNION
                    SELECT
                    m.room_id
                    ,m.start_at
                    ,m.end_at
                    ,m.created_at
                    FROM meeting m
                )
                
                SELECT * FROM room_schedule WHERE room_id = %s AND start_at < %s AND end_at > %s
            """
            cur.execute(qry, (room_id, end_at, start_at,))
            records = cur.fetchall()
            cur.close()
            return records