import psycopg2 as dbapi2

def drop_usertable(getconf):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        query = """DROP TABLE IF EXISTS USERS"""
        cursor.execute(query)
        connection.commit()

def init_usertable(getconf, user):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        query = """CREATE TABLE USERS
                    (
                        ID SERIAL NOT NULL,
                        USERNAME TEXT NOT NULL,
                        PASSWD TEXT NOT NULL,
                        EMAIL TEXT NOT NULL,
                        NAME TEXT NOT NULL,
                        SURNAME TEXT NOT NULL,
                        GENRES TEXT,
                        PROFPIC TEXT,
                        PRIMARY KEY (id)
                    )"""
        cursor.execute(query)

        query = """INSERT INTO USERS
                    (
                        USERNAME, PASSWD, EMAIL, NAME, SURNAME)
                        VALUES (%s, %s, %s, %s, %s
                    )"""
        cursor.execute(query, (user.username, user.passwd, user.email, user.name, user.surname))
        connection.commit()