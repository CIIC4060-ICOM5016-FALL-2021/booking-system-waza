import psycopg2
import psycopg2.extras
from datetime import datetime


class RoomDAO:
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

    @staticmethod
    def addNewRoom(connection, roomtype_id, department_id, name, capacity):
        with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            time_now = datetime.now()
            qry = "INSERT INTO Room (roomtype_id, department_id, name, capacity, created_at) VALUES (%s, %s, %s, %s, %s) RETURNING id"
            cur.execute(qry, (roomtype_id, department_id, name, capacity, time_now))
            connection.commit()
            record_id = cur.fetchone()['id']
            cur.close()
            return record_id

    @staticmethod
    def getRoomById(connection, room_id: int):
        with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            qry = "SELECT * FROM Room WHERE id = %s;"
            cur.execute(qry, ((room_id),))
            record = cur.fetchone()
            cur.close()
            return record

    @staticmethod
    def getAllRooms(connection):
        with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            qry = "SELECT * FROM Room;"
            cur.execute(qry)
            records = cur.fetchall()
            cur.close()
            return records

    @staticmethod
    def deleteRoom(connection, room_id: int):
        with connection.cursor() as cur:
            qry = "DELETE FROM Room WHERE id = %s;"
            cur.execute(qry, (room_id,))
            connection.commit()
            cur.close()

    @staticmethod
    def updateRoom(connection,room_id, roomtype_id, department_id, name, capacity):
        with connection.cursor() as cur:
            qry = "Update Room SET roomtype_id = (%s), department_id = (%s), name = (%s), capacity = (%s) WHERE id = (%s);"
            cur.execute(qry, ((roomtype_id), (department_id), name, capacity, (room_id)))
            connection.commit()
            cur.close()