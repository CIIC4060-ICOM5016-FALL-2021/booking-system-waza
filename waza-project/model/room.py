import psycopg2
import psycopg2.extras
from datetime import datetime


class Room:
    @staticmethod
    def post(connection, roomtype_id, department_id, name, capacity):
        with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            time_now = datetime.now()
            qry = "INSERT INTO Room (roomtype_id, department_id, name, capacity, created_at) VALUES (%s, %s, %s, %s, %s) RETURNING id"
            cur.execute(qry, (roomtype_id, department_id, name, capacity, time_now))
            connection.commit()
            record_id = cur.fetchone()['id']
            cur.close()
            return record_id

    @staticmethod
    def get_first(connection, room_id: int):
        with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            qry = "SELECT * FROM Room WHERE id = %s;"
            cur.execute(qry, (str(room_id)))
            record = cur.fetchone()
            cur.close()
            return record

    @staticmethod
    def get_all(connection):
        with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            qry = "SELECT * FROM Room;"
            cur.execute(qry)
            records = cur.fetchall()
            cur.close()
            return records

    @staticmethod
    def delete(connection, room_id: int):
        with connection.cursor() as cur:
            qry = "DELETE FROM Room WHERE id = %s;"
            cur.execute(qry, str(room_id))
            connection.commit()
            cur.close()

    @staticmethod
    def put(connection,room_id, roomtype_id, department_id, name, capacity):
        with connection.cursor() as cur:
            qry = "Update Room SET roomtype_id = (%s), department_id = (%s), name = (%s), capacity = (%s) WHERE id = (%s);"
            cur.execute(qry, ((roomtype_id), (department_id), name, capacity, (room_id)))
            connection.commit()
            cur.close()