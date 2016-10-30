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
