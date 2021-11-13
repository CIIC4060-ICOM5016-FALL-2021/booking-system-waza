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
                WITH hour_mapper AS (
                    SELECT 1 AS hour, '1am' AS readable_hour
                    UNION
                    SELECT 2 AS hour, '2am' AS readable_hour
                    UNION
                    SELECT 3 AS hour, '3am' AS readable_hour
                    UNION
                    SELECT 4 AS hour, '4am' AS readable_hour
                    UNION
                    SELECT 5 AS hour, '5am' AS readable_hour
                    UNION
                    SELECT 6 AS hour, '6am' AS readable_hour
                    UNION
                    SELECT 7 AS hour, '7am' AS readable_hour
                    UNION
                    SELECT 8 AS hour, '8am' AS readable_hour
                    UNION
                    SELECT 9 AS hour, '9am' AS readable_hour
                    UNION
                    SELECT 10 AS hour, '10am' AS readable_hour
                    UNION
                    SELECT 11 AS hour, '11am' AS readable_hour
                    UNION
                    SELECT 12 AS hour, '12pm' AS readable_hour
                    UNION
                    SELECT 13 AS hour, '1pm' AS readable_hour
                    UNION
                    SELECT 14 AS hour, '2pm' AS readable_hour
                    UNION
                    SELECT 15 AS hour, '3pm' AS readable_hour
                    UNION
                    SELECT 16 AS hour, '4pm' AS readable_hour
                    UNION
                    SELECT 17 AS hour, '5pm' AS readable_hour
                    UNION
                    SELECT 18 AS hour, '6pm' AS readable_hour
                    UNION
                    SELECT 19 AS hour, '7pm' AS readable_hour
                    UNION
                    SELECT 20 AS hour, '8pm' AS readable_hour
                    UNION
                    SELECT 21 AS hour, '9pm' AS readable_hour
                    UNION
                    SELECT 22 AS hour, '10pm' AS readable_hour
                    UNION
                    SELECT 23 AS hour, '11pm' AS readable_hour
                    UNION
                    SELECT 24 AS hour, '12am' AS readable_hour
                )
                
                SELECT
                    h.readable_hour as meeting_hour
                    , count(*)
                FROM Meeting m
                INNER JOIN hour_mapper h
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