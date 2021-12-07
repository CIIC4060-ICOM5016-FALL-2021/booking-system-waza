from config.dbconfig import pg_config
import psycopg2
import psycopg2.extras
from datetime import datetime


class InviteeDAO:
    def __init__(self):
        self.conn = psycopg2.connect(host=pg_config['host'],
                                     port=pg_config['port'],
                                     dbname=pg_config['dbname'],
                                     user=pg_config['user'],
                                     password=pg_config['password'],
                                     )

    def addNewInvitee(self, user_id, meeting_id):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            time_now = datetime.now()
            qry = "INSERT INTO Invitee (user_id, meeting_id, created_at) VALUES (%s, %s, %s) RETURNING id"
            cur.execute(qry, (user_id, meeting_id, time_now,))
            self.conn.commit()
            record_id = cur.fetchone()['id']
            cur.close()
            return record_id

    def getInviteeById(self, iid):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            qry = "SELECT * FROM Invitee WHERE id = %s;"
            cur.execute(qry, (iid,))
            record = cur.fetchone()
            cur.close()
            return record

    def getAllInvitees(self):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            qry = "SELECT * FROM Invitee;"
            cur.execute(qry)
            records = cur.fetchall()
            cur.close()
            return records

    def deleteInvitee(self, iid):
        with self.conn.cursor() as cur:
            qry = "DELETE FROM Invitee WHERE id = %s;"
            cur.execute(qry, (iid,))
            self.conn.commit()
            cur.close()
            return True

    def updateInvitee(self, iid, user_id, meeting_id):
        with self.conn.cursor() as cur:
            qry = "Update Invitee SET user_id = (%s), meeting_id = (%s) WHERE id = (%s);"
            cur.execute(qry, (user_id, meeting_id, iid,))
            self.conn.commit()
            cur.close()
            return True

    def getInviteeByMeetingId(self, mid):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            qry = "SELECT i.*, m.start_at, m.end_at FROM Invitee i LEFT JOIN Meeting m ON i.meeting_id = m.id WHERE meeting_id = %s;"
            cur.execute(qry, (mid,))
            record = cur.fetchone()
            cur.close()
            return record

    # get meetings that has overlaps with provided meeting for an specific user
    def checkInviteeUnavailability(self, user_id, meeting_id):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            qry = """ 
            SELECT 
                i.id
                ,i.user_id
                ,i.meeting_id
                ,m.start_at
                ,m.end_at
                ,i.created_at
            FROM Invitee i
            INNER JOIN Meeting m
                ON i.meeting_id = m.id
            INNER JOIN meeting me -- expected new meet
            ON  me.id = %s AND
            (
                m.start_at < me.end_at
                AND m.end_at > me.start_at
            )
            WHERE user_id = %s"""
            cur.execute(qry, (meeting_id, user_id,))
            records = cur.fetchall()
            cur.close()
            return records


    def getMeetingWithInviteesDetail(self, mid):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            qry = """
            SELECT
                m.id as meeting_id,
                m.start_at,
                m.end_at,
                m.name,
                m.description,
                i.id as invitee_id,
                creator.id as meeting_creator_id,
                creator.first_name as meeting_creator_first_name,
                creator.last_name as meeting_creator_last_name,
                creator.email as meeting_creator_email,
                creator.phone as meeting_creator_phone,
                invited.id as invitee_user_id,
                invited.first_name as invitee_user_first_name,
                invited.last_name as invitee_user_last_name,
                invited.email as invitee_user_email,
                invited.phone as invitee_user_phone
            FROM invitee i
            INNER JOIN meeting m on m.id = i.meeting_id
            INNER JOIN "User" creator on creator.id = m.created_by
            INNER JOIN "User" invited on invited.id = i.user_id
            WHERE m.id = %s;
            """
            cur.execute(qry, (mid,))
            records = cur.fetchall()
            cur.close()
            return records
