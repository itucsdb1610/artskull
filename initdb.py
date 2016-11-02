import psycopg2 as dbapi2


# Start for Muhammed Kadir YÜCEL
def drop_usertable(getconf):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        query = """DROP TABLE IF EXISTS USERS"""
        cursor.execute(query)
        connection.commit()
        cursor.close()

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
                        USERNAME, SALT, HASH, EMAIL, NAME, SURNAME, PROFPIC)
                        VALUES (%s, %s, %s, %s, %s, %s, %s
                    )"""
        cursor.execute(query, (user.username, user.salt, user.hash, user.email, user.name, user.surname, user.profpic))
        connection.commit()
        cursor.close()

def getall_usertable(getconf):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        query = """SELECT NAME, SURNAME, USERNAME, EMAIL, PROFPIC FROM USERS"""
        cursor.execute(query)
        alldata = cursor.fetchall()

        connection.commit()
        cursor.close()

        return alldata

def getuser_usertable(getconf, username):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        query = """SELECT NAME, SURNAME, EMAIL FROM USERS WHERE USERNAME = %s"""
        cursor.execute(query, (username,))
        getuser = cursor.fetchone()

        connection.commit()
        cursor.close()

        return getuser
		
def fixdrop_usertable(getconf):
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
        connection.commit()
        cursor.close()


def deletefrom_usertable(getconf, username):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        query = """DELETE FROM USERS WHERE USERNAME = %s"""
        cursor.execute(query, (username,))
        connection.commit()
        cursor.close()

def edituserwpass_usertable(getconf, user):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        query = """UPDATE USERS SET 
                    NAME = %s,
                    SURNAME = %s,
                    EMAIL = %s,
                    SALT = %s,
                    HASH = %s
                    WHERE USERNAME = %s"""

        cursor.execute(query, (user.name, user.surname, user.email, user.salt, user.hash, user.username,))
        connection.commit()
        cursor.close()

def edituserwopass_usertable(getconf, user):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        query = """UPDATE USERS SET 
                    NAME = %s,
                    SURNAME = %s,
                    EMAIL = %s
                    WHERE USERNAME = %s"""

        cursor.execute(query, (user.name, user.surname, user.email, user.username,))
        connection.commit()
        cursor.close()
# End for Muhammed Kadir YÜCEL

# Start for Murat Özkök
def init_commentTable(getconf):
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
		
		connection.commit()
		cursor.close()
def insert_commenttable(getconf,comment):
	with dbapi2.connect(getconf) as connection:
		cursor = connection.cursor()	
		query="""INSERT INTO COMMENTS
					(
						COMMENT, CONTENTID, USERNAME)
						VALUES(%s, %s, %s
						)"""
		cursor.execute(query, (comment.comm, comment.contentid, comment.username) )
		connection.commit()
		cursor.close()
		
def getall_commenttable(getconf):
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
        query = """SELECT COMMENTID, USERNAME, COMMENT, CONTENTID FROM COMMENTS """
        cursor.execute(query)
        alldata = cursor.fetchall()

        connection.commit()
        cursor.close()

        return alldata	
def edit_comment(getconf, commentid, comment):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        query = """UPDATE COMMENTS SET
                        USERNAME=%s,
						COMMENT=%s,
						CONTENTID=%s
                        WHERE COMMENTID = %s"""

        cursor.execute(query, (comment.username,comment.comm,comment.contentid,commentid))
        connection.commit()
        cursor.close()
def getcomment(getconf,commentid):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
		
        query = """SELECT COMMENTID, USERNAME, COMMENT, CONTENTID FROM COMMENTS WHERE COMMENTID = %s"""
        cursor.execute(query, (commentid,))
        outcomment = cursor.fetchone()

        connection.commit()
        cursor.close()

        return outcomment
			
def deletefrom_commenttable(getconf, commentid):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        query = """DELETE FROM COMMENTS WHERE COMMENTID = %s"""
        cursor.execute(query, (commentid,))
        connection.commit()
        cursor.close()
def drop_commenttable(getconf):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        query = """DROP TABLE IF EXISTS COMMENTS"""
        cursor.execute(query)
        connection.commit()
        cursor.close()
#End for Murat Özkök

# Start for Furkan Özçelik
def init_contenttable(getconf, content):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        query = """CREATE TABLE IF NOT EXISTS CONTENT
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
        cursor.close()

def getall_contenttable(getconf):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        query = """SELECT ID, TITLE, ARTIST, DURATION, DATE, CONTENTPIC, GENRES FROM CONTENT"""
        cursor.execute(query)
        allcontents = cursor.fetchall()

        connection.commit()
        cursor.close()

        return allcontents

def deletefrom_contenttable(getconf, contentid):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        query = """DELETE FROM CONTENT WHERE ID = %s"""
        cursor.execute(query, (contentid,))
        connection.commit()
        cursor.close()

def getcontent_contenttable(getconf, contentid):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        query = """SELECT TITLE, ARTIST, DURATION, DATE, CONTENTPIC, GENRES FROM CONTENT WHERE ID = %s"""
        cursor.execute(query, (contentid,))
        getcontent = cursor.fetchone()

        connection.commit()
        cursor.close()

        return getcontent

def edit_content(getconf, contentid,content):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        query = """UPDATE CONTENT SET
                        TITLE = %s,
                        ARTIST = %s,
                        DURATION = %s,
                        DATE = %s,
                        CONTENTPIC = %s,
                        GENRES = %s
                        WHERE ID = %s"""

        cursor.execute(query, (content.title,content.artist,content.duration,content.date,content.genres,content.contentpic,contentid))
        connection.commit()
        cursor.close()
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

def editactor(getconf, ID, actortoedit):
     with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        query = """UPDATE Actors SET
                        NAME = %s,
                        SURNAME = %s,
                        BIRTHDAY = %s
                        WHERE ActorID = %s"""
        cursor.execute(query, (actortoedit.name, actortoedit.surname, actortoedit.birthday, ID))
        connection.commit()
        cursor.close()

def getall_actortable(getconf):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        query = """SELECT NAME, SURNAME, BIRTHDAY FROM Actors"""
        cursor.execute(query)
        alldata = cursor.fetchall()
        connection.commit()
        cursor.close()

        return alldata

# End for Doğay Kamar

#Start for Mahmut Lutfullah Özbilen

def init_actionTable(getconf):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        query = """CREATE TABLE IF NOT EXISTS ACTIONS
				(
					ACTIONID SERIAL NOT NULL,
					USERNAME TEXT NOT NULL,
					CONTENTID INTEGER NOT NULL,
					ACTIONTYPE TEXT,
                    ACTIONCOMMENT TEXT,
                    DATE TEXT NOT NULL,
                    PRIMARY KEY (ACTIONID)
				)"""				
        cursor.execute(query)
        connection.commit()
        cursor.close()
		
def insert_actionTable(getconf,action):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()		
        query="""INSERT INTO ACTIONS
					(
						USERNAME, CONTENTID, ACTIONTYPE, ACTIONCOMMENT, DATE)
						VALUES(%s, %s, %s, %s, %s
						)"""
        cursor.execute(query, (action.username, action.contentid, action.actiontype, action.actioncomment, action.date) )
        connection.commit()
        cursor.close()

def dropActionTable(getconf):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        query = """DROP TABLE IF EXISTS ACTIONS"""
        cursor.execute(query)
        connection.commit()
        cursor.close()

def getAllActions(getconf):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        query = "SELECT USERNAME, CONTENTID, ACTIONTYPE, ACTIONCOMMENT, DATE FROM ACTIONS"
        cursor.execute(query)
        alldata = cursor.fetchall()

        connection.commit()
        cursor.close()
        return alldata

def getAction(getconf,username):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        query = "SELECT USERNAME, CONTENTID, ACTIONTYPE, ACTIONCOMMENT, DATE FROM ACTIONS WHERE USERNAME = %s"
        cursor.execute(query, (username,))
        action = cursor.fetchone()
        connection.commit()
        cursor.close()
        return action

def edit_Action(getconf,comment,username):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        query = """UPDATE ACTIONS SET ACTIONCOMMENT = %s WHERE USERNAME = %s"""
        cursor.execute(query, (comment,username,))
        connection.commit()
        cursor.close()

def deleteActionFromTable(getconf,username):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        query = """Delete From ACTIONS
                WHERE USERNAME = %s"""
        cursor.execute(query,(username,))
        connection.commit()
        cursor.close()
#end for Mahmut Lutfullah Özbilen