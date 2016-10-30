import psycopg2 as dbapi2


# Start for Muhammed Kadir YÜCEL
def drop_usertable(getconf):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        query = """DROP TABLE IF EXISTS USERS"""
        cursor.execute(query)
        connection.commit()

def init_usertable(getconf, user):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        query = """CREATE TABLE IF NOT EXISTS USERS
                    (
                        ID SERIAL NOT NULL,
                        USERNAME TEXT UNIQUE NOT NULL,
                        SALT TEXT NOT NULL,
                        HASH TEXT NOT NULL, 
                        EMAIL TEXT UNIQUE NOT NULL,
                        NAME TEXT NOT NULL,
                        SURNAME TEXT NOT NULL,
                        GENRES TEXT,
                        PROFPIC TEXT,
                        PRIMARY KEY (id)
                    )"""
        cursor.execute(query)

        query = """INSERT INTO USERS
                    (
                        USERNAME, SALT, HASH, EMAIL, NAME, SURNAME)
                        VALUES (%s, %s, %s, %s, %s, %s
                    )"""
        cursor.execute(query, (user.username, user.salt, user.hash, user.email, user.name, user.surname))
        connection.commit()
# End for Muhammed Kadir YÜCEL

# Start for Murat Özkök
def init_commentTable(getconf,comment):
	with dbapi2.connect(getconf) as connection:
		cursor = connection.cursor()
		query = """CREATE TABLE IF NOT EXISTS COMMENTS
				(
					COMMENTID SERIAL NOT NULL,
					COMMENT TEXT NOT NULL,
					CONTENTID INT NOT NULL,
					USERNAME TEXT NOT NULL
				)"""				
		cursor.execute(query)
		
		
		
		query="""INSERT INTO COMMENTS
					(
						COMMENT, CONTENTID, USERNAME)
						VALUES(%s, %s, %s
						)"""
		cursor.execute(query, (comment.comm, comment.contentid, comment.username) )
		connection.commit()
		
#End for Murat Özkök

# Start for Furkan Özçelik
def init_contenttable(getconf, content):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        query = """CREATE TABLE CONTENT
                    (
                        ID SERIAL NOT NULL,
                        TITLE TEXT NOT NULL,
                        ARTIST TEXT NOT NULL,
                        DURATION TEXT NOT NULL,
                        DATE TEXT NOT NULL,
                        GENRES TEXT,
                        CONTENTPIC TEXT,
                        PRIMARY KEY (id)
                    )"""
        cursor.execute(query)

        query = """INSERT INTO CONTENT
                    (
                        TITLE,ARTIST,DURATION,DATE,GENRES,CONTENTPIC)
                        VALUES (%s, %s, %s, %s, %s,%s
                    )"""
        cursor.execute(query, (content.title,content.artist,content.duration,content.date,content.genres,content.contentpic))
        connection.commit()

# End for Furkan Özçelik

# Start for Doğay Kamar
def init_followerstable(getconf, id1, id2):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        query = """CREATE TABLE IF NOT EXISTS Followers
                    (
                        following_ID INTEGER NOT NULL REFERENCES USERS(ID),
                        following_ID INTEGER NOT NULL REFERENCES USERS(ID),
                        CONSTRAINT pk_FOLLOWERS PRIMARY KEY (following_ID, follower_ID)
                    )"""
        cursor.execute(query)

        query = """INSERT INTO Followers
                    (
                        following_ID, follower_ID)
                        VALUES (%d, %d
                    )"""
        cursor.execute(query, (id1, id2))
        connection.commit()
        cursor.close()

def init_actortable(getconf, name, surname, birthday):
     with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        query = """CREATE TABLE IF NOT EXISTS Actors
                    (
                        ActorID SERIAL NOT NULL,
                        NAME TEXT NOT NULL,
                        SURNAME TEXT NOT NULL,
                        BIRTHDAY TEXT NOT NULL,
                        PRIMARY KEY (ActorID)
                    )"""
        cursor.execute(query)

        query = """INSERT INTO Actors
                    (
                        NAME, SURNAME, BIRTHDAY)
                        VALUES (%s, %s, %s
                    )"""
        cursor.execute(query, (name, surname, birthday))
        connection.commit()
        cursor.close()


def deleteactor(getconf, deleteID):
     with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        query = """DELETE FROM Actors
        WHERE ActorID = %s"""
        cursor.execute(query, (deleteID))
        connection.commit()
        cursor.close()


# End for Doğay Kamar