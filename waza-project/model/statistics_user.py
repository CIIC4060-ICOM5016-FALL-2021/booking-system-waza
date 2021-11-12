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

    def getMostUsedRoomWithUsers(self, user_id):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            qry = """
                SELECT
                    r.name AS room_name
                    ,rt.name AS room_type
                    ,d.name AS department_name
                    ,COUNT(*) AS room_count
                FROM Meeting m
                INNER JOIN Invitee i ON i.user_id=%s AND m.id = i.meeting_id
                LEFT JOIN room r ON r.id = m.room_id
                LEFT JOIN roomtype rt ON r.roomtype_id = rt.id
                LEFT JOIN department d ON r.department_id = d.id
                GROUP BY r.name, rt.name, d.name
                ORDER BY COUNT(*) DESC
                LIMIT 1;
            """
            cur.execute(qry, (user_id, ))
            records = cur.fetchall()
            cur.close()
            return records

    def getMostBookedPeerUsers(self, user_id):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            qry = """
                SELECT
                    u.first_name
                    ,u.last_name
                    ,u.email
                    ,u.phone
                    ,count(*) AS meetings_count
                FROM invitee i
                LEFT JOIN "User" u ON u.id = i.user_id
                WHERE
                    i.user_id <> %s
                    AND i.meeting_id IN
                    (
                        SELECT meeting_id FROM invitee i2 WHERE i2.user_id = %s
                    )
                GROUP BY u.first_name, u.last_name, u.email, u.phone
                ORDER BY COUNT(*) DESC
                LIMIT 1;
            """
            cur.execute(qry, (user_id, user_id, ))
            records = cur.fetchall()
            cur.close()
            return records
