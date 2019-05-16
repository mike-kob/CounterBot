import psycopg2

from models import User
from settings import AUTH_STRING


def user_exists(user: User) -> bool:
    sql = """
          SELECT *
          FROM "user"
          WHERE user_id=%s OR username=%s;
    """
    conn = None

    try:
        conn = psycopg2.connect(AUTH_STRING)

        cur = conn.cursor()
        cur.execute(sql, [user.user_id, user.username])

        res = cur.fetchone()

        cur.close()
        if res is None:
            return False
        else:
            return True

    except (Exception, psycopg2.DatabaseError) as error:
        print('user_exists:', error)
        return False
    finally:
        if conn is not None:
            conn.close()


def save_user(user: User) -> None:
    sql_insert = """
            INSERT INTO "user" (user_id, username, status) 
            VALUES (%s, %s, %s);
        """
    sql_update = """
                UPDATE "user" 
                SET username = %s, status = %s
                WHERE user_id=%s;
            """
    sql_check = """
          SELECT *
          FROM "user"
          WHERE user_id=%s OR username=%s;
    """

    conn = None
    try:
        conn = psycopg2.connect(AUTH_STRING)

        cur = conn.cursor()

        cur.execute(sql_check, [user.user_id, user.username])

        res = cur.fetchone()
        if res is None:
            cur.execute(sql_insert, [user.user_id, user.username, user.status])
            conn.commit()
            cur.close()
        else:
            cur.execute(sql_update, [user.username, user.status, user.user_id])
            conn.commit()
            cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print('save_user:', error)
    finally:
        if conn is not None:
            conn.close()


def get_user(user_id: str) -> User:
    sql_check = """
          SELECT user_id, username, status
          FROM "user"
          WHERE user_id=%s;
    """

    conn = None
    out = None
    try:
        conn = psycopg2.connect(AUTH_STRING)

        cur = conn.cursor()

        cur.execute(sql_check, (user_id,))

        res = cur.fetchone()
        if res is not None:
            out = User(res[0], res[1], res[2])
        return out

    except (Exception, psycopg2.DatabaseError) as error:
        print('get_user:', error)
    finally:
        if conn is not None:
            conn.close()
