import psycopg2

from typing import List
from models import Counter, User
from settings import AUTH_STRING


def save_counter(counter: Counter) -> None:
    sql_insert = """
            INSERT INTO counter (name, value, user_id)
            VALUES (%s, %s, %s);
        """
    sql_update = """
                UPDATE counter
                SET name = %s, value = %s, user_id = %s
                WHERE counter_id=%s;
            """
    sql_check = """
              SELECT *
              FROM counter
              WHERE counter_id=%s;
        """
    conn = None
    try:
        conn = psycopg2.connect(AUTH_STRING)

        cur = conn.cursor()
        cur.execute(sql_check, [counter.counter_id])

        res = cur.fetchone()
        if res is None:
            cur.execute(sql_insert, [counter.name, counter.value, counter.owner.user_id])
            conn.commit()
            cur.close()
        else:
            cur.execute(sql_update, [counter.name, counter.value, counter.owner.user_id, counter.counter_id])
            conn.commit()
            cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print('save_counter:', error)
    finally:
        if conn is not None:
            conn.close()


def get_counter(counter_id: str) -> Counter:
    sql_check = """
          SELECT u.user_id, u.username, u.status, counter_id, name, value
          FROM counter INNER JOIN "user" u on counter.user_id = u.user_id
          WHERE counter_id=%s;
    """

    conn = None
    out = None
    try:
        conn = psycopg2.connect(AUTH_STRING)

        cur = conn.cursor()

        cur.execute(sql_check, (counter_id,))

        res = cur.fetchone()
        if res is not None:
            user = User(res[0], res[1], res[2])
            out = Counter(res[3], res[4], user, res[5])
        return out

    except (Exception, psycopg2.DatabaseError) as error:
        print('get_counter:', error)
    finally:
        if conn is not None:
            conn.close()


def get_user_counters(user: User) -> List[Counter]:
    sql_check = """
          SELECT counter_id, name, value
          FROM counter
          WHERE user_id=%s;
    """

    conn = None
    out = []
    try:
        conn = psycopg2.connect(AUTH_STRING)

        cur = conn.cursor()

        cur.execute(sql_check, (user.user_id,))

        while True:
            res = cur.fetchmany(100)

            if not res:
                break
            else:
                for row in res:
                    out.append(Counter(row[0], row[1], user, row[2]))
        return out

    except (Exception, psycopg2.DatabaseError) as error:
        print('get_counter:', error)
    finally:
        if conn is not None:
            conn.close()