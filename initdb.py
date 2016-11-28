import psycopg2 as dbapi2
import hashlib


# Start for Muhammed Kadir YÜCEL

def init_usertable(getconf, user):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        query = """CREATE TABLE IF NOT EXISTS ACTIONS
				(
					ACTIONID SERIAL NOT NULL,
					USERNAME TEXT NOT NULL,
					CONTENTID INTEGER NOT NULL,
					ACTIONTYPE TEXT,
                    ACTIONCOMMENT TEXT,
                    DATE TIMESTAMP NOT NULL,
                    PRIMARY KEY (ACTIONID)
				)"""				
        cursor.execute(query)
        connection.commit()
        query = """CREATE TABLE IF NOT EXISTS USERS
                    (
                        USERNAME TEXT UNIQUE NOT NULL,
                        SALT TEXT NOT NULL,
                        HASH TEXT NOT NULL, 
                        EMAIL TEXT UNIQUE NOT NULL,
                        NAME TEXT NOT NULL,
                        SURNAME TEXT NOT NULL,
                        PROFPIC TEXT,
                        PRIMARY KEY (USERNAME)
                    )"""
        cursor.execute(query)

        query = """INSERT INTO USERS
                    (
                        USERNAME, SALT, HASH, EMAIL, NAME, SURNAME, PROFPIC)
                        VALUES (%s, %s, %s, %s, %s, %s, %s
                    )"""
        cursor.execute(query, (user.username, user.salt, user.hash, user.email, user.name, user.surname, user.profpic,))
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

        query = """SELECT NAME, SURNAME, EMAIL, PROFPIC FROM USERS WHERE USERNAME = %s"""
        cursor.execute(query, (username,))
        getuser = cursor.fetchone()

        connection.commit()
        cursor.close()

        return getuser


def isuser_intable(getconf, username, password):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        query = """SELECT COUNT(1) FROM USERS WHERE USERNAME = %s"""
        cursor.execute(query, (username,))

        if cursor.fetchone()[0]:
            queryPass = """SELECT SALT, HASH FROM USERS WHERE USERNAME = %s"""
            cursor.execute(queryPass, (username,))
            for row in cursor.fetchall():
                saltedPassword = password.join(row[0])
                hashedPassword = hashlib.md5(saltedPassword.encode()).hexdigest()
                if hashedPassword == row[1]:
                    return True
        else:
            return False

        return False
		
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

def search_user_table(getconf, keyword):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        keyword = '%' + keyword + '%'
        query = """SELECT USERNAME, EMAIL, NAME, SURNAME, PROFPIC FROM USERS WHERE ( (LOWER(USERNAME) LIKE LOWER(%s)) OR
                    (LOWER(EMAIL) LIKE LOWER(%s)) OR (LOWER(NAME) LIKE LOWER(%s) ) OR (LOWER(SURNAME) LIKE LOWER(%s)))"""
        cursor.execute(query, (keyword,keyword,keyword,keyword,))
        alldata = cursor.fetchall()

        connection.commit()
        cursor.close()

        return alldata

def edituserwpass_usertable(getconf, user):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        query = """UPDATE USERS SET 
                    NAME = %s,
                    SURNAME = %s,
                    EMAIL = %s,
                    SALT = %s,
                    HASH = %s,
                    PROFPIC = %s
                    WHERE USERNAME = %s"""

        cursor.execute(query, (user.name, user.surname, user.email, user.salt, user.hash, user.profpic, user.username,))
        connection.commit()
        cursor.close()

def edituserwopass_usertable(getconf, user):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        query = """UPDATE USERS SET 
                    NAME = %s,
                    SURNAME = %s,
                    EMAIL = %s,
                    PROFPIC = %s
                    WHERE USERNAME = %s"""

        cursor.execute(query, (user.name, user.surname, user.email, user.profpic, user.username,))
        connection.commit()
        cursor.close()

def init_followUserUser(getconf, getfollower, getfollowed, getdate):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        query = """CREATE TABLE IF NOT EXISTS USERFOLLOW
                    (
                        FOLLOWER TEXT NOT NULL REFERENCES USERS(USERNAME) ON DELETE CASCADE,
                        FOLLOWED TEXT NOT NULL REFERENCES USERS(USERNAME) ON DELETE CASCADE,
                        FOLLOWDATE TIMESTAMP NOT NULL,
                        PRIMARY KEY(FOLLOWER, FOLLOWED)
                    )"""
        
        cursor.execute(query)

        query = """INSERT INTO USERFOLLOW
                    (
                        FOLLOWER, FOLLOWED, FOLLOWDATE)
                        VALUES(%s,%s,%s
                    )"""
        cursor.execute(query, (getfollower, getfollowed, getdate,))
        connection.commit()
        cursor.close()

def unfollow_followUserUser(getconf, getfollower, getfollowed):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        query = """CREATE TABLE IF NOT EXISTS USERFOLLOW
                    (
                        FOLLOWER TEXT NOT NULL REFERENCES USERS(USERNAME) ON DELETE CASCADE,
                        FOLLOWED TEXT NOT NULL REFERENCES USERS(USERNAME) ON DELETE CASCADE,
                        FOLLOWDATE TIMESTAMP NOT NULL,
                        PRIMARY KEY(FOLLOWER, FOLLOWED)
                    )"""
        
        cursor.execute(query)

        query = """DELETE FROM USERFOLLOW WHERE (
                    FOLLOWER = %s AND
                    FOLLOWED = %s
                    )
                    """
        cursor.execute(query, (getfollower, getfollowed,))
        connection.commit()
        cursor.close()

def get_allfollowing(getconf, getfollower):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        query = """CREATE TABLE IF NOT EXISTS USERFOLLOW
                    (
                        FOLLOWER TEXT NOT NULL REFERENCES USERS(USERNAME) ON DELETE CASCADE,
                        FOLLOWED TEXT NOT NULL REFERENCES USERS(USERNAME) ON DELETE CASCADE,
                        FOLLOWDATE TIMESTAMP NOT NULL,
                        PRIMARY KEY(FOLLOWER, FOLLOWED)
                    )"""
        
        cursor.execute(query)

        query = """SELECT NAME, SURNAME, EMAIL, USERNAME, PROFPIC, FOLLOWDATE FROM USERS, USERFOLLOW WHERE
                    ((USERS.USERNAME = USERFOLLOW.FOLLOWED) AND (USERFOLLOW.FOLLOWER = %s))"""
        cursor.execute(query, (getfollower,))
        alldata = cursor.fetchall()

        connection.commit()
        cursor.close()

        return alldata

def get_allfollower(getconf, getfollowed):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        query = """CREATE TABLE IF NOT EXISTS USERFOLLOW
                    (
                        FOLLOWER TEXT NOT NULL REFERENCES USERS(USERNAME) ON DELETE CASCADE,
                        FOLLOWED TEXT NOT NULL REFERENCES USERS(USERNAME) ON DELETE CASCADE,
                        FOLLOWDATE TIMESTAMP NOT NULL,
                        PRIMARY KEY(FOLLOWER, FOLLOWED)
                    )"""
        
        cursor.execute(query)

        query = """SELECT NAME, SURNAME, EMAIL, USERNAME, PROFPIC, FOLLOWDATE FROM USERS, USERFOLLOW WHERE
                    ((USERS.USERNAME = USERFOLLOW.FOLLOWER) AND (USERFOLLOW.FOLLOWED = %s))"""
        cursor.execute(query, (getfollowed,))
        alldata = cursor.fetchall()

        connection.commit()
        cursor.close()

        return alldata

def get_followed_counts(getconf, getfollowed):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        query = """CREATE TABLE IF NOT EXISTS USERFOLLOW
                    (
                        FOLLOWER TEXT NOT NULL REFERENCES USERS(USERNAME) ON DELETE CASCADE,
                        FOLLOWED TEXT NOT NULL REFERENCES USERS(USERNAME) ON DELETE CASCADE,
                        FOLLOWDATE TIMESTAMP NOT NULL,
                        PRIMARY KEY(FOLLOWER, FOLLOWED)
                    )"""
        
        cursor.execute(query)

        query = """SELECT COUNT(FOLLOWER) FROM USERFOLLOW WHERE FOLLOWED = %s"""
        cursor.execute(query, (getfollowed,))
        returnnumber = cursor.fetchone()[0]

        connection.commit()
        cursor.close()

        return returnnumber

def get_following_counts(getconf, getfollower):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        query = """CREATE TABLE IF NOT EXISTS USERFOLLOW
                    (
                        FOLLOWER TEXT NOT NULL REFERENCES USERS(USERNAME) ON DELETE CASCADE,
                        FOLLOWED TEXT NOT NULL REFERENCES USERS(USERNAME) ON DELETE CASCADE,
                        FOLLOWDATE TIMESTAMP NOT NULL,
                        PRIMARY KEY(FOLLOWER, FOLLOWED)
                    )"""
        
        cursor.execute(query)

        query = """SELECT COUNT(FOLLOWED) FROM USERFOLLOW WHERE FOLLOWER = %s"""
        cursor.execute(query, (getfollower,))
        returnnumber = cursor.fetchone()[0]

        connection.commit()
        cursor.close()

        return returnnumber

def is_following(getconf, getfollower, getfollowed):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        query = """CREATE TABLE IF NOT EXISTS USERFOLLOW
                    (
                        FOLLOWER TEXT NOT NULL REFERENCES USERS(USERNAME) ON DELETE CASCADE,
                        FOLLOWED TEXT NOT NULL REFERENCES USERS(USERNAME) ON DELETE CASCADE,
                        FOLLOWDATE TIMESTAMP NOT NULL,
                        PRIMARY KEY(FOLLOWER, FOLLOWED)
                    )"""
        
        cursor.execute(query)

        query = """SELECT COUNT(*) FROM USERFOLLOW WHERE ((FOLLOWER = %s) AND (FOLLOWED =%s))"""
        cursor.execute(query, (getfollower, getfollowed,))
        returnnumber = cursor.fetchone()[0]

        if returnnumber == 0:
            return False
        else:
            return True


def init_genreTable(getconf, getusername, getgenre, getorder):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        
        query = """CREATE TABLE IF NOT EXISTS USERGENRES
                    (
                        USERNAME TEXT NOT NULL REFERENCES USERS(USERNAME) ON DELETE CASCADE,
                        GENRE TEXT NOT NULL,
                        IMPORTANCE INTEGER NOT NULL,
                        PRIMARY KEY(USERNAME, GENRE) 
                    )"""
        
        cursor.execute(query)

        query = """INSERT INTO USERGENRES
                    (
                        USERNAME, GENRE, IMPORTANCE)
                        VALUES (%s, %s, %s
                    )"""
        cursor.execute(query, (getusername, getgenre, getorder,))
        connection.commit()
        cursor.close()

def update_genreTable(getconf, username, genre, order):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        query = """UPDATE USERGENRES SET 
                    IMPORTANCE = %s
                    WHERE ((USERNAME = %s) AND (GENRE = %s))"""

        cursor.execute(query, (order,username,genre,))
        connection.commit()
        cursor.close()


def getall_genres(getconf, username):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        query = """CREATE TABLE IF NOT EXISTS USERGENRES
                    (
                        USERNAME TEXT NOT NULL REFERENCES USERS(USERNAME) ON DELETE CASCADE,
                        GENRE TEXT NOT NULL,
                        IMPORTANCE INTEGER NOT NULL,
                        PRIMARY KEY(USERNAME, GENRE)
                    )"""
        
        cursor.execute(query)

        query = """SELECT GENRE, IMPORTANCE FROM USERGENRES WHERE USERNAME = %s ORDER BY IMPORTANCE DESC"""        
        cursor.execute(query, (username,))
        alldata = cursor.fetchall()

        connection.commit()
        cursor.close()

        return alldata

def getone_genre(getconf, username, genre):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        query = """CREATE TABLE IF NOT EXISTS USERGENRES
                    (
                        USERNAME TEXT NOT NULL REFERENCES USERS(USERNAME) ON DELETE CASCADE,
                        GENRE TEXT NOT NULL,
                        IMPORTANCE INTEGER NOT NULL,
                        PRIMARY KEY(USERNAME, GENRE)
                    )"""
        
        cursor.execute(query)

        query = """SELECT GENRE, IMPORTANCE FROM USERGENRES WHERE ((USERNAME = %s) AND (GENRE = %s))"""
        cursor.execute(query, (username,genre,))
        alldata = cursor.fetchone()

        connection.commit()
        cursor.close()

        return alldata

def delete_genreTable(getconf, username, genre):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        query = """DELETE FROM USERGENRES WHERE (USERNAME = %s AND GENRE = %s)"""
        cursor.execute(query, (username, genre,))
        connection.commit()
        cursor.close()

# End for Muhammed Kadir YÜCEL

# Start for Murat Özkök
def init_commentTable(getconf):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        query = """CREATE TABLE IF NOT EXISTS ACTIONS
				(
                    ACTIONID SERIAL NOT NULL,
                    USERNAME TEXT NOT NULL,
                    CONTENTID INTEGER NOT NULL REFERENCES CONTENT (id) ON DELETE CASCADE,
                    ACTIONTYPE TEXT,
                    ACTIONCOMMENT TEXT,
                    DATE TIMESTAMP NOT NULL,
                    PRIMARY KEY (ACTIONID)
				)"""				
        cursor.execute(query)
        connection.commit()
		
        cursor = connection.cursor()
        query = """CREATE TABLE IF NOT EXISTS COMMENTS
				(
					COMMENTID SERIAL NOT NULL,
					COMMENT TEXT NOT NULL,
					ACTIONID INT NOT NULL REFERENCES ACTIONS (actionid) ON DELETE CASCADE,
					USERNAME TEXT NOT NULL REFERENCES USERS (username) ON DELETE CASCADE,
					PRIMARY KEY (commentid)
				)"""				
        cursor.execute(query)
		
        connection.commit()
        cursor.close()
def insert_commenttable(getconf,comment):
	with dbapi2.connect(getconf) as connection:
		cursor = connection.cursor()	
		query="""INSERT INTO COMMENTS
					(
						COMMENT, ACTIONID, USERNAME)
						VALUES(%s, %s, %s
						)"""
		cursor.execute(query, (comment.comm, comment.actionid, comment.username,) )
		connection.commit()
		cursor.close()
		
def getall_commenttable(getconf):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        query = """CREATE TABLE IF NOT EXISTS COMMENTS
                (
                    COMMENTID SERIAL NOT NULL,
                    COMMENT TEXT NOT NULL,
                    ACTIONID INT NOT NULL REFERENCES ACTIONS (actionid) ON DELETE CASCADE,
                    USERNAME TEXT NOT NULL REFERENCES USERS (username) ON DELETE CASCADE,
					PRIMARY KEY (commentid)
                )"""				
        cursor.execute(query)
        query = """SELECT COMMENTID, USERNAME, COMMENT, ACTIONID FROM COMMENTS """
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
						ACTIONID=%s
                        WHERE COMMENTID = %s"""

        cursor.execute(query, (comment.username,comment.comm,comment.actionid,commentid))
        connection.commit()
        cursor.close()
def getcomment(getconf,commentid):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
		
        query = """SELECT COMMENTID, USERNAME, COMMENT, ACTIONID FROM COMMENTS WHERE COMMENTID = %s"""
        cursor.execute(query, (commentid,))
        outcomment = cursor.fetchall()

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


def searchactor(getconf, actortosearch):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        query = """SELECT NAME, SURNAME, BIRTHDAY, ActorID FROM Actors
                    WHERE NAME = %s OR SURNAME = %s"""
        cursor.execute(query, (actortosearch, actortosearch))
        searchdata = cursor.fetchall()
        connection.commit()
        cursor.close()

        return searchdata


def searchactor_byid(getconf, actorid):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        query = """SELECT NAME, SURNAME, BIRTHDAY, ActorID FROM Actors
                    WHERE ActorID = %s"""
        cursor.execute(query, (actorid))
        searchdata = cursor.fetchone()
        connection.commit()
        cursor.close()

        return searchdata


def getall_actortable(getconf):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        query = """SELECT NAME, SURNAME, BIRTHDAY, ActorID FROM Actors"""
        cursor.execute(query)
        alldata = cursor.fetchall()
        connection.commit()
        cursor.close()

        return alldata


def init_casting(getconf):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        query = """CREATE TABLE IF NOT EXISTS CASTING
                    (
                        ActorID INTEGER NOT NULL REFERENCES Actors(ActorID),
                        ContentID INTEGER NOT NULL REFERENCES CONTENT(ID),
                        ORD INTEGER NOT NULL,
                        PRIMARY KEY(ActorID, ContentID)
                    )"""

        cursor.execute(query)
        connection.commit()
        cursor.close()


def insert_casting(getconf, actorid, contentid, ord):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        query = """INSERT INTO CASTING
                            (
                                ActorID, ContentID, ORD)
                                VALUES (%s, %s, %s
                            )"""
        cursor.execute(query, (actorid, contentid, ord))
        connection.commit()
        cursor.close()


def deletecast(getconf, deleteIDa, deleteIDc):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        query = """DELETE FROM CASTING
        WHERE ActorID = %s AND ContentID = %s"""
        cursor.execute(query, (deleteIDa, deleteIDc))
        connection.commit()
        cursor.close()


def editcast(getconf, actorid, contentid, ord):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        query = """UPDATE CASTING SET
                        ORD = %s
                        WHERE ActorID = %s AND ContentID = %s"""
        cursor.execute(query, (ord, actorid, contentid))
        connection.commit()
        cursor.close()


def searchcast(getconf, casttosearch):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        query = """SELECT NAME, SURNAME, BIRTHDAY, Actors.ActorID, ORD FROM Actors, CASTING
                    WHERE (ContentID = %s AND Actors.ActorID = CASTING.ActorID)
                    ORDER BY ORD ASC"""
        cursor.execute(query, (casttosearch))
        searchdata = cursor.fetchall()
        connection.commit()
        cursor.close()

        return searchdata


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
                    DATE TIMESTAMP NOT NULL,
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

        query = """CREATE TABLE IF NOT EXISTS USERFOLLOW
                    (
                        FOLLOWER TEXT NOT NULL REFERENCES USERS(USERNAME) ON DELETE CASCADE,
                        FOLLOWED TEXT NOT NULL REFERENCES USERS(USERNAME) ON DELETE CASCADE,
                        FOLLOWDATE TIMESTAMP NOT NULL,
                        PRIMARY KEY(FOLLOWER, FOLLOWED)
                    )"""
        
        cursor.execute(query)

        query = """SELECT USERNAME, CONTENTID, ACTIONTYPE, ACTIONCOMMENT, DATE, ACTIONID FROM ACTIONS
                    WHERE USERNAME = %s 
                    OR USERNAME IN (SELECT FOLLOWED FROM USERFOLLOW
                                            WHERE FOLLOWER = %s)
                    ORDER BY 5 DESC"""
        username2 = username
        cursor.execute(query, (username,username2))
        action = cursor.fetchall()
        connection.commit()
        cursor.close()
        return action
        
def edit_Action(getconf,comment,actionid):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        query = """UPDATE ACTIONS SET ACTIONCOMMENT = %s WHERE ACTIONID = %s"""
        cursor.execute(query, (comment,actionid,))
        connection.commit()
        cursor.close()

def deleteActionFromTable(getconf,actionid):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        query = """Delete From ACTIONS
                WHERE ACTIONID = %s"""
        cursor.execute(query,(actionid,))
        connection.commit()
        cursor.close()

def getcontent_action(getconf,contentid):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        query = "SELECT USERNAME, CONTENTID, ACTIONTYPE, ACTIONCOMMENT, DATE FROM ACTIONS WHERE CONTENTID = %s ORDER BY 5 DESC"
        cursor.execute(query, (contentid,))
        action = cursor.fetchall()
        connection.commit()
        cursor.close()
        return action

def  getActionContent(getconf):#for timeline
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        query = """SELECT ID, TITLE, ARTIST, DURATION, DATE, CONTENTPIC, GENRES FROM CONTENT"""
        cursor.execute(query)
        content = cursor.fetchall()
        connection.commit()
        cursor.close()
        return content
#end for Mahmut Lutfullah Özbilen
