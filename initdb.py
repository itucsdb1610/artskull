import psycopg2 as dbapi2
import hashlib


# Start for Muhammed Kadir YÜCEL
def init_adminstable(getconf):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_usertable(getconf)
        query = """CREATE TABLE IF NOT EXISTS ADMINS
                (
                    ADMINUSERNAME TEXT NOT NULL REFERENCES USERS(USERNAME) ON DELETE CASCADE ON UPDATE CASCADE,
                    ADMINORDER INTEGER NOT NULL,
                    PRIMARY KEY(ADMINUSERNAME, ADMINORDER)
                )"""
        
        
        cursor.execute(query)
        connection.commit()
        insert_firstadmin(getconf)
        cursor.close()

def insert_firstadmin(getconf):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        query = """SELECT COUNT(*) FROM ADMINS WHERE ADMINUSERNAME = 'admin'"""

        cursor.execute(query)
        count = cursor.fetchone()[0]

        if count == 0:
            query = """INSERT INTO USERS (USERNAME, SALT, HASH, EMAIL, NAME, SURNAME, PROFPIC) VALUES (
                        'admin', 'gclS5B3IG9BnyvOM', 'd35e0a09e4bdb940ddb6174b8e71db11', 'admin@artskull.com', 'Website', 'Admin', 'http://www.sbsc.in/images/dummy-profile-pic.png'
                    )"""
            cursor.execute(query)
            query = """INSERT INTO ADMINS (ADMINUSERNAME, ADMINORDER) VALUES ('admin', 0)"""
            cursor.execute(query)

        connection.commit()
        cursor.close()

def insert_adminstable(getconf, username, order):
    with dbapi2.connect(getconf) as connection:
        init_adminstable(getconf)
        cursor = connection.cursor()
        
        query = """INSERT INTO ADMINS
                (
                    ADMINUSERNAME, ADMINORDER) VALUES (
                        %s, %s
                )"""
        cursor.execute(query, (username, order,))
        connection.commit()
        cursor.close()

def remove_adminstable(getconf, username):
    with dbapi2.connect(getconf) as connection:
        init_adminstable(getconf)
        cursor = connection.cursor()

        query = """DELETE FROM ADMINS WHERE (ADMINUSERNAME = %s)"""
        cursor.execute(query, (username,))
        connection.commit()
        cursor.close()

def update_adminstable(getconf, username, order):
    with dbapi2.connect(getconf) as connection:
        init_adminstable(getconf)
        cursor = connection.cursor()

        query = """UPDATE ADMINS SET
                    ODER = %s WHERE ADMINUSERNAME = %s"""

        cursor.execute(query, (order,username,))
        connection.commit()
        cursor.close()

def getall_adminstable(getconf):
    with dbapi2.connect(getconf) as connection:
        init_adminstable(getconf)

        cursor = connection.cursor()

        query = """SELECT * FROM ADMINS"""

        cursor.execute(query)
        alldata = cursor.fetchall()

        connection.commit()
        cursor.close()

        return alldata

def getspecific_admistable(getconf, username):
    with dbapi2.connect(getconf) as connection:
        init_adminstable(getconf)

        cursor = connection.cursor()

        query = """SELECT * FROM ADMINS WHERE ADMINUSERNAME = %s"""

        cursor.execute(query, (username,))
        getdata = cursor.fetchone()

        connection.commit()
        cursor.close()

        return getdata

def isAdmin_userEdit(getconf, username):
    with dbapi2.connect(getconf) as connection:
        init_adminstable(getconf)

        cursor = connection.cursor()
        print(username)
        query = """SELECT COUNT(*) FROM ADMINS WHERE (ADMINUSERNAME = %s)"""
        cursor.execute(query, (username,))
        returnnumber = cursor.fetchone()[0]

        if returnnumber == 0:
            return False
        else:
            return True

def init_usertable(getconf):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
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
        connection.commit()
        cursor.close()

def insert_userstable(getconf, user):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_usertable(getconf)
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

        query = """SELECT NAME, SURNAME, USERNAME, EMAIL, PROFPIC FROM USERS ORDER BY NAME"""
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
                    (LOWER(EMAIL) LIKE LOWER(%s)) OR (LOWER(NAME) LIKE LOWER(%s) ) OR (LOWER(SURNAME) LIKE LOWER(%s))) ORDER BY NAME"""
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

def initonly_followUserUser(getconf):
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
        connection.commit()
        cursor.close()

def init_followUserUser(getconf, getfollower, getfollowed, getdate):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        initonly_followUserUser(getconf)

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
        initonly_followUserUser(getconf)
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

        initonly_followUserUser(getconf)

        query = """SELECT NAME, SURNAME, EMAIL, USERNAME, PROFPIC, FOLLOWDATE FROM USERS, USERFOLLOW WHERE
                    ((USERS.USERNAME = USERFOLLOW.FOLLOWED) AND (USERFOLLOW.FOLLOWER = %s)) ORDER BY FOLLOWDATE"""
        cursor.execute(query, (getfollower,))
        alldata = cursor.fetchall()

        connection.commit()
        cursor.close()

        return alldata

def get_allfollower(getconf, getfollowed):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        initonly_followUserUser(getconf)

        query = """SELECT NAME, SURNAME, EMAIL, USERNAME, PROFPIC, FOLLOWDATE FROM USERS, USERFOLLOW WHERE
                    ((USERS.USERNAME = USERFOLLOW.FOLLOWER) AND (USERFOLLOW.FOLLOWED = %s)) ORDER BY FOLLOWDATE"""
        cursor.execute(query, (getfollowed,))
        alldata = cursor.fetchall()

        connection.commit()
        cursor.close()

        return alldata

def get_followed_counts(getconf, getfollowed):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        initonly_followUserUser(getconf)
        query = """SELECT COUNT(FOLLOWER) FROM USERFOLLOW WHERE FOLLOWED = %s"""
        cursor.execute(query, (getfollowed,))
        returnnumber = cursor.fetchone()[0]

        connection.commit()
        cursor.close()

        return returnnumber

def get_following_counts(getconf, getfollower):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        initonly_followUserUser(getconf)

        query = """SELECT COUNT(FOLLOWED) FROM USERFOLLOW WHERE FOLLOWER = %s"""
        cursor.execute(query, (getfollower,))
        returnnumber = cursor.fetchone()[0]

        connection.commit()
        cursor.close()

        return returnnumber

def is_following(getconf, getfollower, getfollowed):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        initonly_followUserUser(getconf)

        query = """SELECT COUNT(*) FROM USERFOLLOW WHERE ((FOLLOWER = %s) AND (FOLLOWED =%s))"""
        cursor.execute(query, (getfollower, getfollowed,))
        returnnumber = cursor.fetchone()[0]

        if returnnumber == 0:
            return False
        else:
            return True

def initonly_genreTable(getconf):
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
        connection.commit()
        cursor.close()

def init_genreTable(getconf, getusername, getgenre, getorder):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        initonly_genreTable(getconf)
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

        initonly_genreTable(getconf)

        query = """SELECT GENRE, IMPORTANCE FROM USERGENRES WHERE USERNAME = %s ORDER BY IMPORTANCE DESC"""        
        cursor.execute(query, (username,))
        alldata = cursor.fetchall()

        connection.commit()
        cursor.close()

        return alldata

def getone_genre(getconf, username, genre):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        initonly_genreTable(getconf)

        query = """SELECT GENRE, IMPORTANCE FROM USERGENRES WHERE ((USERNAME = %s) AND (GENRE = %s))"""
        cursor.execute(query, (username,genre,))
        alldata = cursor.fetchone()

        connection.commit()
        cursor.close()

        return alldata

def delete_genreTable(getconf, username, genre):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        initonly_genreTable(getconf)
        query = """DELETE FROM USERGENRES WHERE (USERNAME = %s AND GENRE = %s)"""
        cursor.execute(query, (username, genre,))
        connection.commit()
        cursor.close()

# End for Muhammed Kadir YÜCEL

# Start for Murat Özkök
def init_commentTable(getconf):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_actionTable(getconf)
        cursor = connection.cursor()
        query = """CREATE TABLE IF NOT EXISTS COMMENTS
				(
					COMMENTID SERIAL NOT NULL,
					COMMENT TEXT NOT NULL,
					ACTIONID INT NOT NULL REFERENCES ACTIONS (actionid) ON DELETE CASCADE,
					USERNAME TEXT NOT NULL REFERENCES USERS (username) ON DELETE CASCADE,
                    DATE TIMESTAMP NOT NULL,
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
						COMMENT, ACTIONID, USERNAME, DATE)
						VALUES(%s, %s, %s, %s
						) RETURNING COMMENTID"""
        cursor.execute(query, (comment.comm, comment.actionid, comment.username, comment.date))
        id = cursor.fetchall()
        connection.commit()
        cursor.close()
        id = id[0]
        return id
		
def getall_commenttable(getconf):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_commentTable(getconf)
        query = """SELECT COMMENTID, COMMENTS.USERNAME, COMMENT, ACTIONID, NAME, SURNAME ,PROFPIC, DATE FROM COMMENTS,USERS WHERE (COMMENTS.USERNAME=USERS.USERNAME) ORDER BY 7 DESC """
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
		
        query = """SELECT COMMENTID, USERNAME, COMMENT, ACTIONID, DATE FROM COMMENTS WHERE COMMENTID = %s"""
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
def delete_comments_from_action(getconf,actionid):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        query = """DELETE FROM COMMENTS WHERE ACTIONID = %s"""
        cursor.execute(query, (actionid,))
        connection.commit()
        cursor.close()  
def actionid_of_comment(getconf,commentid):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        query = "SELECT ACTIONID FROM COMMENTS WHERE COMMENTID = %s"    
        cursor.execute(query,(commentid,))
        actid = cursor.fetchall()
        connection.commit()
        cursor.close()     
        actid = actid[0]
        return actid   
def username_of_comment(getconf,commentid):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        query = "SELECT USERNAME FROM COMMENTS WHERE COMMENTID = %s"    
        cursor.execute(query,(commentid,))
        username = cursor.fetchall()
        connection.commit()
        cursor.close()   
        username = username[0]
        return username   

def init_reportstable(getconf):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        query="""CREATE TABLE IF NOT EXISTS REPORTS
                (
                    ID SERIAL NOT NULL,
                    REPORTTEXT TEXT NOT NULL,
                    COMMENTID INT NOT NULL REFERENCES COMMENTS(COMMENTID) ON DELETE CASCADE,
                    USERNAME TEXT NOT NULL REFERENCES USERS(USERNAME) ON DELETE CASCADE,
                    DATE TIMESTAMP NOT NULL,
                    PRIMARY KEY (id)
                )"""
        cursor.execute(query)
        connection.commit()
        cursor.close()

def insert_reports(getconf,report):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_reportstable(getconf)
        query="""INSERT INTO REPORTS
                    (
                        REPORTTEXT, COMMENTID, USERNAME, DATE)
                        VALUES(%s, %s, %s, %s
                        )"""
        cursor.execute(query, (report.reporttext, report.commentid, report.username, report.date) )
        connection.commit()
        cursor.close()    
def getall_reports(getconf):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_reportstable(getconf)
        query = """SELECT REPORTS.ID, REPORTS.REPORTTEXT, REPORTS.COMMENTID, REPORTS.USERNAME, COMMENTS.COMMENT DATE FROM REPORTS, COMMENTS WHERE ( REPORTS.COMMENTID = COMMENTS.COMMENTID )    """
        cursor.execute(query)
        alldata = cursor.fetchall()

        connection.commit()
        cursor.close()

        return alldata	
        
def deleteFromReport(getconf, id):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_reportstable(getconf)
        query = "DELETE FROM REPORTS WHERE ID = %s"
        cursor.execute(query,(id,))
        connection.commit()
        cursor.close
def drop_reports(getconf):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        query = """DROP TABLE IF EXISTS REPORTS"""
        cursor.execute(query)
        connection.commit()
        cursor.close()    
def username_of_action(getconf, actionid):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_actionTable(getconf)
        query = "SELECT USERNAME FROM ACTIONS WHERE ACTIONID = %s"    
        cursor.execute(query,(actionid,))
        username = cursor.fetchall()
        connection.commit()
        cursor.close()   
        username = username[0]
        return username   
def init_notifications(getconf):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        query = """CREATE TABLE IF NOT EXISTS NOTIFICATIONS
                (
                    ID SERIAL NOT NULL,
                    COMMENTID INT NOT NULL REFERENCES COMMENTS(COMMENTID) ON DELETE CASCADE,
                    COMMENTER TEXT NOT NULL REFERENCES USERS(USERNAME) ON DELETE CASCADE,
                    RECEIVER TEXT NOT NULL REFERENCES USERS(USERNAME) ON DELETE CASCADE,
                    DATE TIMESTAMP NOT NULL,
                    ISREAD BOOLEAN NOT NULL,
                    PRIMARY KEY (id)
                )   """ 
        cursor.execute(query)
        query = """ALTER TABLE NOTIFICATIONS ALTER COLUMN ISREAD SET DEFAULT false"""
        cursor.execute(query)
        connection.commit()
        cursor.close()

def insert_notifications(getconf, notification):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_notifications(getconf)
        query="""INSERT INTO NOTIFICATIONS
                    (
                        COMMENTID, COMMENTER, RECEIVER, DATE)
                        VALUES(%s, %s, %s, %s
                        )"""
        cursor.execute(query, (notification.commentid, notification.commenter, notification.receiver, notification.date) )
        connection.commit()
        cursor.close()  
def get_notifications(getconf, username):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_notifications(getconf)
        query="""SELECT USERS.NAME, USERS.SURNAME, COMMENTS.COMMENT, ACTIONID, NOTIFICATIONS.DATE, ISREAD, NOTIFICATIONS.ID, 
        RECEIVER, COMMENTER
        FROM NOTIFICATIONS, COMMENTS, USERS WHERE USERS.USERNAME = COMMENTER AND  COMMENTS.COMMENTID = NOTIFICATIONS.COMMENTID AND RECEIVER != COMMENTER
            AND RECEIVER = %s
        ORDER BY NOTIFICATIONS.DATE DESC """
        cursor.execute(query,(username,))
        alldata = cursor.fetchall()
        
        connection.commit()
        cursor.close()
        return alldata
def make_read(getconf,id):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_notifications(getconf)
        query = """UPDATE NOTIFICATIONS SET
                        ISREAD = true
                        WHERE ID = %s"""

        cursor.execute(query, (id,))
        connection.commit()
        cursor.close()      
def make_all_read(getconf, username):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_notifications(getconf)
        query = """UPDATE NOTIFICATIONS SET
                        ISREAD = true
                        WHERE RECEIVER = %s"""

        cursor.execute(query, (username,))
        connection.commit()
        cursor.close()   
#End for Murat Özkök

# Start for Furkan Özçelik
def init_furkanstables(getconf):
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

        query = """CREATE TABLE IF NOT EXISTS STAGE
                            (
                                STAGEID SERIAL NOT NULL,
                                NAME TEXT NOT NULL,
                                 LOCATION TEXT NOT NULL,
                              CAPACITY TEXT NOT NULL,
                                STAGEPIC TEXT NOT NULL,
                                 PRIMARY KEY (STAGEID)
                            )"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS PLAY
                             (
                                    STAGEID INTEGER REFERENCES STAGE(STAGEID)
                                    ON DELETE CASCADE
                                    ON UPDATE CASCADE,
                                    CONTENTID INTEGER REFERENCES CONTENT(ID)
                                    ON DELETE CASCADE
                                    ON UPDATE CASCADE,
                                    DATE TEXT NOT NULL,
                                     PRIMARY KEY (STAGEID,CONTENTID)
                              )"""
        cursor.execute(query)


        connection.commit()
        cursor.close()

def init_contenttable(getconf, content):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        init_furkanstables(getconf)

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
        init_furkanstables(getconf)
        query = """SELECT ID, TITLE, ARTIST, DURATION, DATE, CONTENTPIC, GENRES FROM CONTENT"""
        cursor.execute(query)
        allcontents = cursor.fetchall()

        connection.commit()
        cursor.close()

        return allcontents

def deletefrom_contenttable(getconf, contentid):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_furkanstables(getconf)
        query = """DELETE FROM CONTENT WHERE ID = %s"""
        cursor.execute(query, (contentid,))
        connection.commit()
        cursor.close()

def getcontent_contenttable(getconf, contentid):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_furkanstables(getconf)
        query = """SELECT TITLE, ARTIST, DURATION, DATE, CONTENTPIC, GENRES FROM CONTENT WHERE ID = %s"""
        cursor.execute(query, (contentid,))
        getcontent = cursor.fetchone()

        connection.commit()
        cursor.close()

        return getcontent

def edit_content(getconf, contentid,content):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_furkanstables(getconf)
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

def init_stagetable(getconf, stage):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        init_furkanstables(getconf)

        query = """INSERT INTO STAGE
                   (
                        NAME,LOCATION,CAPACITY,STAGEPIC)
                          VALUES (%s, %s, %s, %s
                     )"""
        cursor.execute(query, (
        stage.name,stage.location,stage.capacity,stage.stagepic))
        connection.commit()
        cursor.close()

def getall_stagestable(getconf):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_furkanstables(getconf)
        query = """SELECT STAGEID,NAME,LOCATION,CAPACITY,STAGEPIC FROM STAGE"""
        cursor.execute(query)
        allstages = cursor.fetchall()

        connection.commit()
        cursor.close()

        return allstages

def deletefrom_stagetable(getconf, stageid):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_furkanstables(getconf)
        query = """DELETE FROM STAGE WHERE STAGEID = %s"""
        cursor.execute(query, (stageid,))
        connection.commit()
        cursor.close()

def getstage_stagetable(getconf, stageid):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_furkanstables(getconf)
        query = """SELECT STAGEID,NAME,LOCATION,CAPACITY,STAGEPIC FROM STAGE WHERE STAGEID = %s"""
        cursor.execute(query, (stageid,))
        getstage = cursor.fetchone()

        connection.commit()
        cursor.close()

        return getstage

def edit_stage(getconf, stageid, stage):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_furkanstables(getconf)
        query = """UPDATE STAGE SET
                            NAME = %s,
                            LOCATION = %s,
                            CAPACITY = %s,
                            STAGEPIC = %s
                            WHERE STAGEID = %s"""

        cursor.execute(query, (
            stage.name, stage.location, stage.capacity, stage.stagepic,
        stageid))
        connection.commit()
        cursor.close()

def init_playtable(getconf, stageid,contentid,date):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        init_furkanstables(getconf)

        query = """INSERT INTO PLAY
                       (
                            STAGEID,CONTENTID,DATE)
                              VALUES (%s, %s, %s
                         )"""
        cursor.execute(query, (
            stageid, contentid, date))
        connection.commit()
        cursor.close()

def getall_playstable(getconf):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_furkanstables(getconf)
        query = """SELECT PLAY.STAGEID,PLAY.CONTENTID,PLAY.DATE,STAGE.NAME,CONTENT.TITLE FROM PLAY,CONTENT,STAGE WHERE (PLAY.CONTENTID=CONTENT.ID) AND (STAGE.STAGEID=PLAY.STAGEID);"""
        cursor.execute(query)
        allplays = cursor.fetchall()

        connection.commit()
        cursor.close()

        return allplays

def deletefrom_playtable(getconf, stageid,contentid):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_furkanstables(getconf)
        query = """DELETE FROM PLAY WHERE (STAGEID = %s) AND (CONTENTID = %s)"""
        cursor.execute(query, (stageid,contentid,))
        connection.commit()
        cursor.close()

def getplay_playtable(getconf, stageid,contentid):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_furkanstables(getconf)
        query = """SELECT STAGEID,CONTENTID,DATE FROM PLAY WHERE (STAGEID = %s) AND (CONTENTID= %s) """
        cursor.execute(query, (stageid,contentid,))
        getplay = cursor.fetchone()

        connection.commit()
        cursor.close()

        return getplay

def edit_play(getconf, stageid,contentid,stageidn,contentidn,date):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_furkanstables(getconf)
        query = """UPDATE PLAY SET
                            STAGEID = %s,
                            CONTENTID = %s,
                            DATE = %s
                            WHERE (STAGEID = %s) AND (CONTENTID = %s)"""

        cursor.execute(query, (
            stageidn, contentidn, date, stageid, contentid,))
        connection.commit()
        cursor.close()

def findstages(getconf,contentid):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_furkanstables(getconf)
        query = """SELECT NAME,LOCATION,CAPACITY,STAGEPIC,PLAY.STAGEID,PLAY.DATE FROM CONTENT,PLAY,STAGE
        WHERE ((CONTENT.ID=PLAY.CONTENTID) AND (STAGE.STAGEID=PLAY.STAGEID) AND (CONTENT.ID=%s));
                         """
        cursor.execute(query,(contentid,))
        getstage = cursor.fetchall()

        connection.commit()
        cursor.close()

        return getstage

def search_content_table(getconf, keyword):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_furkanstables(getconf)
        keyword = '%' + keyword + '%'
        query = """SELECT ID, TITLE, ARTIST, DURATION, DATE, CONTENTPIC, GENRES FROM CONTENT WHERE ( (LOWER(TITLE) LIKE LOWER(%s)) OR
                        (LOWER(ARTIST) LIKE LOWER(%s)) OR (LOWER(GENRES) LIKE LOWER(%s))) ORDER BY TITLE"""
        cursor.execute(query, (keyword, keyword, keyword,))
        alldata = cursor.fetchall()

        connection.commit()
        cursor.close()

        return alldata
# End for Furkan Özçelik

# Start for Doğay Kamar
def init_actortablenoadd(getconf):
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
        connection.commit()
        cursor.close()

def init_actortable(getconf, name, surname, birthday):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        init_actortablenoadd(getconf)

        query = """INSERT INTO Actors
                    (
                        NAME, SURNAME, BIRTHDAY)
                        VALUES (%s, %s, %s
                    )"""
        cursor.execute(query, (name, surname, birthday,))
        connection.commit()
        cursor.close()


def deleteactor(getconf, deleteID):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_actortablenoadd(getconf)
        query = """DELETE FROM Actors
        WHERE ActorID = %s"""
        cursor.execute(query, (deleteID,))
        connection.commit()
        cursor.close()


def editactor(getconf, ID, actortoedit):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_actortablenoadd(getconf)
        query = """UPDATE Actors SET
                        NAME = %s,
                        SURNAME = %s,
                        BIRTHDAY = %s
                        WHERE ActorID = %s"""
        cursor.execute(query, (actortoedit.name, actortoedit.surname, actortoedit.birthday, ID,))
        connection.commit()
        cursor.close()


def searchactor(getconf, actortosearch):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_actortablenoadd(getconf)
        query = """SELECT NAME, SURNAME, BIRTHDAY, ActorID FROM Actors
                    WHERE NAME = %s OR SURNAME = %s"""
        cursor.execute(query, (actortosearch, actortosearch,))
        searchdata = cursor.fetchall()
        connection.commit()
        cursor.close()

        return searchdata


def searchactor_byid(getconf, actorid):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_actortablenoadd(getconf)
        query = """SELECT NAME, SURNAME, BIRTHDAY, ActorID FROM Actors
                    WHERE ActorID = %s"""
        cursor.execute(query, (actorid,))
        searchdata = cursor.fetchone()
        connection.commit()
        cursor.close()

        return searchdata


def getall_actortable(getconf):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_actortablenoadd(getconf)
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
                        ActorID INTEGER NOT NULL REFERENCES Actors(ActorID) ON DELETE CASCADE,
                        ContentID INTEGER NOT NULL REFERENCES CONTENT(ID) ON DELETE CASCADE,
                        ORD INTEGER NOT NULL,
                        PRIMARY KEY(ActorID, ContentID)
                    )"""

        cursor.execute(query)
        connection.commit()
        cursor.close()


def insert_casting(getconf, actorid, contentid, ord):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_casting(getconf)
        query = """INSERT INTO CASTING
                            (
                                ActorID, ContentID, ORD)
                                VALUES (%s, %s, %s
                            )"""
        cursor.execute(query, (actorid, contentid, ord,))
        connection.commit()
        cursor.close()


def deletecast(getconf, deleteIDa, deleteIDc):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_casting(getconf)
        query = """DELETE FROM CASTING
        WHERE ActorID = %s AND ContentID = %s"""
        cursor.execute(query, (deleteIDa, deleteIDc,))
        connection.commit()
        cursor.close()


def editcast(getconf, actorid, contentid, ord):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_casting(getconf)
        query = """UPDATE CASTING SET
                        ORD = %s
                        WHERE ActorID = %s AND ContentID = %s"""
        cursor.execute(query, (ord, actorid, contentid,))
        connection.commit()
        cursor.close()


def searchcast(getconf, casttosearch):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_casting(getconf)
        query = """SELECT NAME, SURNAME, BIRTHDAY, Actors.ActorID, ORD FROM Actors, CASTING
                    WHERE (ContentID = %s AND Actors.ActorID = CASTING.ActorID)
                    ORDER BY ORD ASC"""
        cursor.execute(query, (casttosearch,))
        searchdata = cursor.fetchall()
        connection.commit()
        cursor.close()

        return searchdata


def init_rating(getconf):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()

        query = """CREATE TABLE IF NOT EXISTS RATING
                    (
                        Username TEXT NOT NULL REFERENCES USERS(USERNAME) ON DELETE CASCADE,
                        ContentID INTEGER NOT NULL REFERENCES CONTENT(ID) ON DELETE CASCADE,
                        Rate INTEGER NOT NULL,
                        PRIMARY KEY(Username, ContentID)
                    )"""

        cursor.execute(query)
        connection.commit()
        cursor.close()

def insert_rating(getconf, user, contentid, rate):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_rating(getconf)
        query = """INSERT INTO RATING
                            (
                                Username, ContentID, Rate)
                                VALUES (%s, %s, %s
                            )"""
        cursor.execute(query, (user, contentid, rate,))
        connection.commit()
        cursor.close()

def deleterating(getconf, deleteuser, deleteID):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_rating(getconf)
        query = """DELETE FROM RATING
        WHERE Username = %s AND ContentID = %s"""
        cursor.execute(query, (deleteuser, deleteID,))
        connection.commit()
        cursor.close()

def editrating(getconf, user, contentid, rate):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_rating(getconf)
        query = """UPDATE RATING SET
                        Rate = %s
                        WHERE Username = %s AND ContentID = %s"""
        cursor.execute(query, (rate, user, contentid,))
        connection.commit()
        cursor.close()
def israted(getconf, user, contentid):
     with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_rating(getconf)
        query = """SELECT COUNT(*) FROM RATING
                        WHERE (Username = %s AND ContentID = %s)"""
        cursor.execute(query, (user, contentid,))
        result = cursor.fetchone()[0]
        connection.commit()
        cursor.close()
        if result  == 0:
            return False
        else:
            return True
def countvotes(getconf, contentid):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_rating(getconf)
        query = """SELECT COUNT(*) FROM RATING
                        WHERE ContentID = %s"""
        cursor.execute(query, (contentid,))
        result = cursor.fetchone()[0]
        connection.commit()
        cursor.close()
        return result

def getvotes(getconf, contentid):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_rating(getconf)
        query = """SELECT Rate FROM RATING
                        WHERE ContentID = %s"""
        cursor.execute(query, (contentid,))
        result = cursor.fetchall()
        connection.commit()
        cursor.close()
        return result

def getonevote(getconf, user, contentid):
     with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_rating(getconf)
        query = """SELECT Rate FROM RATING
                        WHERE (Username = %s AND ContentID = %s)"""
        cursor.execute(query, (user, contentid,))
        result = cursor.fetchall()
        connection.commit()
        cursor.close()
        return result


# End for Doğay Kamar

#Start for Mahmut Lutfullah Özbilen

def init_actionTable(getconf):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_furkanstables(getconf)
        query = """CREATE TABLE IF NOT EXISTS ACTIONS
				(
					ACTIONID SERIAL NOT NULL,
					USERNAME TEXT NOT NULL REFERENCES USERS(USERNAME) ON DELETE CASCADE,
					CONTENTID INTEGER NOT NULL REFERENCES CONTENT(ID) ON DELETE CASCADE,
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
        init_actionTable(getconf)
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
        query = """DROP TABLE IF EXISTS ACTIONS CASCADE"""
        cursor.execute(query)
        connection.commit()
        cursor.close()

def getAllActions(getconf):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_actionTable(getconf)
        query = "SELECT USERNAME, CONTENTID, ACTIONTYPE, ACTIONCOMMENT, DATE FROM ACTIONS"
        cursor.execute(query)
        alldata = cursor.fetchall()

        connection.commit()
        cursor.close()
        return alldata

def getAction(getconf,username):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_actionTable(getconf)
        initonly_followUserUser(getconf)

        query = """SELECT ACTIONS.USERNAME, CONTENTID, ACTIONTYPE, ACTIONCOMMENT, DATE, ACTIONID, NAME, SURNAME, PROFPIC FROM ACTIONS, USERS
                    WHERE (ACTIONS.USERNAME = %s
                    OR ACTIONS.USERNAME IN (SELECT FOLLOWED FROM USERFOLLOW
                                            WHERE FOLLOWER = %s)) AND ACTIONS.USERNAME = USERS.USERNAME
                    ORDER BY 5 DESC"""
        username2 = username
        cursor.execute(query, (username,username2,))
        action = cursor.fetchall()
        connection.commit()
        cursor.close()
        return action
        
def edit_Action(getconf,comment,actionid):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_actionTable(getconf)
        query = """UPDATE ACTIONS SET ACTIONCOMMENT = %s WHERE ACTIONID = %s"""
        cursor.execute(query, (comment,actionid,))
        connection.commit()
        cursor.close()

def deleteActionFromTable(getconf,actionid):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_actionTable(getconf)
        query = """Delete From ACTIONS
                WHERE ACTIONID = %s"""
        cursor.execute(query,(actionid,))
        connection.commit()
        cursor.close()

def getcontent_action(getconf,contentid):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_actionTable(getconf)
        query = "SELECT ACTIONS.USERNAME, CONTENTID, ACTIONTYPE, ACTIONCOMMENT, DATE,NAME,SURNAME,PROFPIC FROM ACTIONS,USERS WHERE (CONTENTID = %s) AND (ACTIONS.USERNAME=USERS.USERNAME) ORDER BY 5 DESC"
        cursor.execute(query, (contentid,))
        action = cursor.fetchall()
        connection.commit()
        cursor.close()
        return action

def  getActionContent(getconf):#for timeline
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_furkanstables(getconf)
        query = """SELECT ID, TITLE, ARTIST, DURATION, DATE, CONTENTPIC, GENRES FROM CONTENT"""
        cursor.execute(query)
        content = cursor.fetchall()
        connection.commit()
        cursor.close()
        return content

def getuser_action(getconf,username):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_furkanstables(getconf)
        init_actionTable(getconf)
        query = "SELECT ACTIONCOMMENT,ACTIONS.DATE,ACTIONS.CONTENTID,TITLE,CONTENTPIC,ARTIST, ACTIONS.USERNAME, ACTIONID FROM ACTIONS,CONTENT WHERE(ACTIONS.USERNAME = %s AND CONTENT.ID=ACTIONS.CONTENTID)"
        cursor.execute(query,(username,))
        data = cursor.fetchall()
        connection.commit()
        cursor.close()
        return data 

def getEditAction(getconf,actionid):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_actionTable(getconf)
        query = "SELECT ACTIONCOMMENT FROM ACTIONS WHERE ACTIONID = %s"
        cursor.execute(query,(actionid,))
        data = cursor.fetchone()
        connection.commit()
        cursor.close()
        return data

def init_criticTable(getconf):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        query = """CREATE TABLE IF NOT EXISTS CRITIC
				(
					CRITICID SERIAL NOT NULL,
					NAME TEXT NOT NULL,
                    SURNAME TEXT NOT NULL,
                    WORKPLACE TEXT NULL,
                    PROFPIC TEXT,
                    PRIMARY KEY (CRITICID)
				)"""
        cursor.execute(query)
        connection.commit()
        cursor.close()

def insert_criticTable(getconf,criticname,criticsurname,criticworkplace,criticprofpic):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_criticTable(getconf)
        query = """INSERT INTO CRITIC
					(
						NAME, SURNAME, WORKPLACE,PROFPIC)
						VALUES(%s, %s, %s,%s
						)"""
        cursor.execute(query, (criticname,criticsurname,criticworkplace,criticprofpic))
        connection.commit()
        cursor.close()

def getall_critictable(getconf):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_criticTable(getconf)
        query = "SELECT NAME, SURNAME, WORKPLACE, CRITICID, PROFPIC FROM CRITIC"
        cursor.execute(query)
        alldata = cursor.fetchall()

        connection.commit()
        cursor.close()
        return alldata

def edit_critic(getconf,criticid,criticname,criticsurname,criticworkplace,criticprofpic):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_criticTable(getconf)
        query = """UPDATE CRITIC SET 
                    NAME = %s, 
                    SURNAME = %s,
                    WORKPLACE = %s,
                    PROFPIC = %s
                    WHERE CRITICID = %s"""
        cursor.execute(query, (criticname,criticsurname,criticworkplace,criticprofpic,criticid,))
        connection.commit()
        cursor.close()    

def deleteCriticFromTable(getconf,criticid):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_criticTable(getconf)
        query = """Delete From CRITIC
                WHERE CRITICID = %s"""
        cursor.execute(query,(criticid,))
        connection.commit()
        cursor.close()

def init_reviewTable(getconf):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        query = """CREATE TABLE IF NOT EXISTS REVIEW
				(
					REVIEWID SERIAL NOT NULL,
                    CRITICID INTEGER NOT NULL REFERENCES CRITIC(CRITICID) ON DELETE CASCADE,
                    CONTENTID INTEGER NOT NULL REFERENCES CONTENT(ID) ON DELETE CASCADE,
					REVIEW TEXT NOT NULL,
                    DATE TEXT NOT NULL,
                    SCORE INTEGER NOT NULL,
                    PRIMARY KEY (REVIEWID),
                    CHECK ((SCORE >= 0) AND (SCORE <= 100))
				)"""
        cursor.execute(query)
        connection.commit()
        cursor.close()

def insert_reviewTable(getconf,criticid,contentid,review,date,score):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_reviewTable(getconf)
        query = """INSERT INTO REVIEW
					(
						CRITICID, CONTENTID, REVIEW, DATE,SCORE)
						VALUES(%s, %s, %s, %s, %s
						)
        
        """
        cursor.execute(query, (criticid,contentid,review,date,score))
        connection.commit()
        cursor.close()

def getreview_content(getconf,contentid):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_reviewTable(getconf)
        query = """SELECT NAME, SURNAME, WORKPLACE, REVIEW, DATE,SCORE,PROFPIC,REVIEWID,REVIEW.CRITICID FROM REVIEW, CRITIC WHERE ((CONTENTID = %s) AND (REVIEW.CRITICID = CRITIC.CRITICID))
        
        """
        cursor.execute(query, (contentid,))
        alldata = cursor.fetchall()
        connection.commit()
        cursor.close()
        return alldata

def edit_reviewTable(getconf,criticid,review,date,score,reviewid):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_reviewTable(getconf)
        query = """UPDATE REVIEW SET 
                    CRITICID = %s, 
                    REVIEW = %s,
                    DATE = %s,
                    SCORE = %s
                    WHERE REVIEWID = %s"""
        cursor.execute(query, (criticid,review,date,score,reviewid,))
        connection.commit()
        cursor.close()

def deleteReviewFromTable(getconf,reviewid):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_reviewTable(getconf)
        query = """Delete From REVIEW
                WHERE REVIEWID = %s"""
        cursor.execute(query,(reviewid,))
        connection.commit()
        cursor.close()

def getcriticfromtable(getconf,criticid):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_criticTable(getconf)
        query = """SELECT * FROM CRITIC WHERE CRITICID = %s"""

        cursor.execute(query, (criticid,))
        getdata = cursor.fetchone()

        connection.commit()
        cursor.close()

        return getdata

def getReviewofCritic(getconf,criticid):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        query = """SELECT REVIEW, REVIEW.DATE,SCORE,ID, TITLE, ARTIST, CONTENTPIC, REVIEWID FROM REVIEW, CONTENT WHERE ((CRITICID = %s) AND (REVIEW.CONTENTID = CONTENT.ID))
        
        """
        cursor.execute(query, (criticid,))
        alldata = cursor.fetchall()
        connection.commit()
        cursor.close()
        return alldata

def getCurrentcritic(getconf,criticid):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_criticTable(getconf)
        query = """SELECT * FROM CRITIC WHERE CRITICID = %s"""
        cursor.execute(query,(criticid,))
        data = cursor.fetchone()
        connection.commit()
        cursor.close()
        return data

def getCurrentReview(getconf,reviewid):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_reviewTable(getconf)
        query = """SELECT * FROM REVIEW WHERE REVIEWID = %s"""
        cursor.execute(query,(reviewid,))
        data = cursor.fetchone()
        connection.commit()
        cursor.close()
        return data

def getMetaScore(getconf,contentid):
    with dbapi2.connect(getconf) as connection:
        cursor = connection.cursor()
        init_reviewTable(getconf)
        query = """SELECT AVG(SCORE) FROM REVIEW WHERE CONTENTID = %s"""
        cursor.execute(query,(contentid,))
        data = cursor.fetchone()
        connection.commit()
        cursor.close()
        return data

#end for Mahmut Lutfullah Özbilen
