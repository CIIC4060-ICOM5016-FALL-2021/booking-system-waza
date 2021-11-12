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
                h.hour as meeting_hour
                , count(*)
            FROM Meeting m
            INNER JOIN statistics_hours h
                on h.hour >= CAST(TO_CHAR(m.start_at, 'HH24') AS INT)
                       and h.hour < CAST(TO_CHAR(m.end_at, 'HH24') AS INT) -- dont consider the end time, because it is not an hour that may not be used completely
            GROUP BY meeting_hour
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
                u.first_name
                ,u.last_name
                ,u.email
                ,u.phone
                ,count(*)
            FROM Invitee i
            LEFT JOIN "User" u on i.user_id = U.id
            GROUP BY u.first_name, u.last_name, u.email, u.phone, i.user_id
            order by count(*) desc
            LIMIT 10;
            """
            cur.execute(qry)
            records = cur.fetchall()
            cur.close()
            return records

    def getMostBookedRooms(self):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            qry = """
            SELECT
                r.name as room_name
                ,rt.name AS room_type
                ,d.name as department_name
                , count(*)
            FROM Meeting m
            LEFT JOIN room r ON r.id = m.room_id
            LEFT JOIN roomtype rt ON r.roomtype_id = rt.id
            LEFT JOIN department d ON r.department_id = d.id
            GROUP BY r.name, rt.name, d.name
            ORDER BY count(*) DESC
            LIMIT 10;
            """
            cur.execute(qry)
            records = cur.fetchall()
            cur.close()
            return records