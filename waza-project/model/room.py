from config.dbconfig import pg_config
import psycopg2
import psycopg2.extras
from datetime import datetime


class RoomDAO:
    def __init__(self):
        self.conn = psycopg2.connect(host=pg_config['host'],
                                     port=pg_config['port'],
                                     dbname=pg_config['dbname'],
                                     user=pg_config['user'],
                                     password=pg_config['password'],
                                     )

    def addNewRoom(self, roomtype_id, department_id, name, capacity):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            time_now = datetime.now()
            qry = "INSERT INTO Room (roomtype_id, department_id, name, capacity, created_at) VALUES (%s, %s, %s, %s, %s) RETURNING id"
            cur.execute(qry, (roomtype_id, department_id, name, capacity, time_now))
            self.conn.commit()
            record_id = cur.fetchone()['id']
            cur.close()
            return record_id

    def getRoomById(self, room_id):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            qry = "SELECT * FROM Room WHERE id = %s;"
            cur.execute(qry, ((room_id),))
            record = cur.fetchone()
            cur.close()
            return record

    def getAllRooms(self):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            qry = "SELECT * FROM Room;"
            cur.execute(qry)
            records = cur.fetchall()
            cur.close()
            return records

    def deleteRoom(self, room_id):
        with self.conn.cursor() as cur:
            qry = "DELETE FROM Room WHERE id = %s;"
            cur.execute(qry, (room_id,))
            self.conn.commit()
            cur.close()


    def updateRoom(self,room_id, roomtype_id, department_id, name, capacity):
        with self.conn.cursor() as cur:
            qry = "Update Room SET roomtype_id = (%s), department_id = (%s), name = (%s), capacity = (%s) WHERE id = (%s);"
            cur.execute(qry, ((roomtype_id), (department_id), name, capacity, (room_id)))
            self.conn.commit()
            cur.close()


    def getRoomCapacityAvailableByMeeting(self, meeting_id):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            qry = """
                SELECT
                    max(r.capacity) - count(DISTINCT user_id) AS available_capacity
                FROM invitee
                INNER JOIN meeting m on m.id = invitee.meeting_id
                INNER JOIN room r on r.id = m.room_id
                WHERE meeting_id = %s
            """
            cur.execute(qry, (meeting_id,))
            record = cur.fetchone()
            cur.close()
            return record
