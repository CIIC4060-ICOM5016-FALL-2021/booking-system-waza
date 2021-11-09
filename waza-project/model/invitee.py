import psycopg2
import psycopg2.extras
from datetime import datetime


class Invitee:
    @staticmethod
    def post(connection, user_id, meeting_id):
        with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            time_now = datetime.now()
            qry = "INSERT INTO Invitee (user_id, meeting_id, created_at) VALUES (%s, %s, %s) RETURNING id"
            cur.execute(qry, (user_id, meeting_id, time_now,))
            connection.commit()
            record_id = cur.fetchone()['id']
            cur.close()
            return record_id

    @staticmethod
    def get_first(connection, invitee_id: int):
        with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            qry = "SELECT * FROM Invitee WHERE id = %s;"
            cur.execute(qry, (str(invitee_id),))
            record = cur.fetchone()
            cur.close()
            return record

    @staticmethod
    def get_all(connection):
        with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            qry = "SELECT * FROM Invitee;"
            cur.execute(qry)
            records = cur.fetchall()
            cur.close()
            return records

    @staticmethod
    def delete(connection, invitee_id: int):
        with connection.cursor() as cur:
            qry = "DELETE FROM Invitee WHERE id = %s;"
            cur.execute(qry, (str(invitee_id),))
            connection.commit()
            cur.close()

    @staticmethod
    def put(connection, invitee_id, user_id, meeting_id):
        with connection.cursor() as cur:
            qry = "Update Invitee SET user_id = (%s), meeting_id = (%s) WHERE id = (%s);"
            cur.execute(qry, (user_id, meeting_id, invitee_id,))
            connection.commit()
            cur.close()

