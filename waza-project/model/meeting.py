import psycopg2
import psycopg2.extras
from datetime import datetime


class Meeting:
    @staticmethod
    def post(connection, created_by, room_id, start_at, end_at):
        with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            time_now = datetime.now()
            qry = "INSERT INTO Meeting (created_by, room_id, start_at, end_at, created_at) VALUES (%s, %s, %s, %s, %s) RETURNING id"
            cur.execute(qry, (created_by, room_id, start_at, end_at, time_now))
            connection.commit()
            record_id = cur.fetchone()['id']
            cur.close()
            return record_id

    @staticmethod
    def get_first(connection, meeting_id: int):
        with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            qry = "SELECT * FROM Meeting WHERE id = %s;"
            cur.execute(qry, (str(meeting_id),))
            record = cur.fetchone()
            cur.close()
            return record

    @staticmethod
    def get_all(connection):
        with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            qry = "SELECT * FROM Meeting;"
            cur.execute(qry)
            records = cur.fetchall()
            cur.close()
            return records

    @staticmethod
    def delete(connection, meeting_id: int):
        with connection.cursor() as cur:
            qry = "DELETE FROM Meeting WHERE id = %s;"
            cur.execute(qry, (str(meeting_id),))
            connection.commit()
            cur.close()

    @staticmethod
    def put(connection, meeting_id, created_by, room_id, start_at, end_at):
        with connection.cursor() as cur:
            qry = "Update Meeting SET created_by = (%s), room_id = (%s), start_at = (%s), end_at = (%s) WHERE id = (%s);"
            cur.execute(qry, ((created_by), (room_id), start_at, end_at, (meeting_id)))
            connection.commit()
            cur.close()