from config.dbconfig import pg_config
import psycopg2
import psycopg2.extras


class StatisticsGlobalDAO:
    def __init__(self):
        self.conn = psycopg2.connect(host=pg_config['host'],
                                     port=pg_config['port'],
                                     dbname=pg_config['dbname'],
                                     user=pg_config['user'],
                                     password=pg_config['password'],
                                     )

    def getBusiestHours(self):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            qry = """
                SELECT
                    h.hour, count(*)
                FROM Meeting m
                INNER JOIN statistics_hours h
                    on h.hour >= CAST(TO_CHAR(m.start_at, 'HH24') AS INT)
                           and h.hour < CAST(TO_CHAR(m.end_at, 'HH24') AS INT) -- dont consider the end time, because it is not an hour that may not be used completely
                GROUP BY H.hour
                ORDER BY count(*) DESC
                LIMIT 5;
            """
            cur.execute(qry)
            records = cur.fetchall()
            cur.close()
            return records

    def getMostBookedUsers(self):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            qry = """
                SELECT
                    i.user_id, count(*) 
                FROM Invitee i
                GROUP BY i.user_id
                order by count(*) desc
                LIMIT 10
            """
            cur.execute(qry)
            records = cur.fetchall()
            cur.close()
            return records

    def getMostBookedRooms(self):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            qry = """
                SELECT
                    m.room_id, count(*) 
                FROM Meeting m
                GROUP BY m.room_id
                ORDER BY count(*) DESC
                LIMIT 10
            """
            cur.execute(qry)
            records = cur.fetchall()
            cur.close()
            return records