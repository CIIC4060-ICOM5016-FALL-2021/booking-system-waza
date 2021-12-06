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

    def addNewUser(self, role_id, first_name, last_name, email, phone):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            time_now = datetime.now()
            qry = "INSERT INTO \"User\" (role_id, first_name, last_name, email, phone, created_at) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id"
            cur.execute(qry, (role_id, first_name, last_name, email, phone, time_now))
            self.conn.commit()
            record_id = cur.fetchone()['id']
            cur.close()
            return record_id

    def getUserById(self, user_id):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            qry = "SELECT * FROM \"User\" WHERE id = %s;"
            cur.execute(qry, (user_id,))
            record = cur.fetchone()
            cur.close()
            return record

    def getUserLoginValidation(self, user_email, user_pw):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            qry = "SELECT id FROM \"User\" WHERE email = %s AND password = %s;"
            cur.execute(qry, (user_email,user_pw,))
            record = cur.fetchone()
            cur.close()
            return record

    def getAllUsers(self):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            qry = "SELECT * FROM \"User\";"
            cur.execute(qry)
            records = cur.fetchall()
            cur.close()
            return records

    def deleteUser(self, mid):
        with self.conn.cursor() as cur:
            qry = "DELETE FROM \"User\" WHERE id = %s;"
            cur.execute(qry, (mid,))
            self.conn.commit()
            cur.close()
            return True

    def updateUser(self, uid, role_id, first_name, last_name, email, phone,):
        with self.conn.cursor() as cur:
            qry = "Update \"User\" SET role_id = (%s), first_name = (%s), last_name = (%s), email = (%s), phone = (%s) WHERE id = (%s);"
            cur.execute(qry, (role_id, first_name, last_name, email, phone, uid, ))
            self.conn.commit()
            cur.close()
            return True

    def usersAvailabilitySlot(self, users):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            first_user = users[0]
            users = tuple(users)
            qry = """
            WITH all_availability AS (
                SELECT
                start_at
                ,end_at
                ,user_id
                FROM invitee i
                inner join meeting m on m.id = i.meeting_id
                WHERE i.user_id IN %s
                UNION
                SELECT
                start_at
                ,end_at
                ,user_id
                FROM userschedule us
                WHERE us.user_id IN %s
                UNION
                SELECT current_date + INTERVAL '1 month', current_date + INTERVAL '1 month 1 min', %s -- force to make a gap if there are no meets within a month
            )
            , find_date_gaps AS (
                SELECT
                    a.start_at,
                    lag(a.end_at) OVER (PARTITION BY a.user_id ORDER BY a.start_at) as previous_end_at
                FROM all_availability a
            )
            
            SELECT
                g.previous_end_at as start_at,
                g.start_at as end_at
            FROM find_date_gaps g
            WHERE g.start_at > previous_end_at
            ORDER BY start_at
            """
            cur.execute(qry, (users, users, first_user,))
            record = cur.fetchall()
            cur.close()
            return record
