from config.dbconfig import pg_config
import psycopg2
import psycopg2.extras


class StatisticsUserDAO:
    def __init__(self):
        self.conn = psycopg2.connect(host=pg_config['host'],
                                     port=pg_config['port'],
                                     dbname=pg_config['dbname'],
                                     user=pg_config['user'],
                                     password=pg_config['password'],
                                     )

    def getMostUsedRoomWithUsers(self):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            qry = """
                SELECT
                    i.user_id, m.room_id, count(*) as room_count
                FROM Meeting m
                INNER JOIN Invitee i on m.id = i.meeting_id --get only records with invitees
                GROUP BY i.user_id, m.room_id
                order by count(*) desc
            """
            cur.execute(qry)
            records = cur.fetchall()
            cur.close()
            return records

    def getMostBookedUsers(self):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            qry = """
                SELECT
                       user_id, count(*) AS meetings_count
                FROM Meeting
                INNER JOIN Invitee i on meeting.id = i.meeting_id --get only records with invitees
                GROUP BY i.user_id
                order by count(*) desc
            """
            cur.execute(qry)
            records = cur.fetchall()
            cur.close()
            return records
