Parts Implemented by Murat Özkök
================================
Comments Table
-----------

Create table query of COMMENTS table:

.. code-block:: sql
	CREATE TABLE IF NOT EXISTS COMMENTS
					(
						COMMENTID SERIAL NOT NULL,
						COMMENT TEXT NOT NULL,
						ACTIONID INT NOT NULL REFERENCES ACTIONS (actionid) ON DELETE CASCADE,
						USERNAME TEXT NOT NULL REFERENCES USERS (username) ON DELETE CASCADE,
						DATE TIMESTAMP NOT NULL,
						PRIMARY KEY (commentid)
					)
          
          
Comments table uses references of Actions and Users table. Action ID determines where the comment is written. Comment ID is the primary key of table.

Insert to comments table:

.. code-block:: sql
	INSERT INTO COMMENTS
			(
							COMMENT, ACTIONID, USERNAME, DATE)
							VALUES(%s, %s, %s, %s
		    ) RETURNING COMMENTID
      
Returning value is needed in timeline to insert to Notifications table.

Select all comments query:

.. code-block:: sql
	SELECT COMMENTID, COMMENTS.USERNAME, COMMENT, ACTIONID, NAME, SURNAME ,PROFPIC, DATE FROM COMMENTS,USERS WHERE (COMMENTS.USERNAME=USERS.USERNAME) ORDER BY 7 DESC 

Users table is added to this query since name and surname of commenter user will be shown in comment section. 

Select a comment with comment id query:

.. code-block:: sql
	SELECT COMMENTID, USERNAME, COMMENT, ACTIONID, DATE FROM COMMENTS WHERE COMMENTID = %s

Username of commenter is selected with this query:

.. code-block:: sql
	SELECT USERNAME FROM COMMENTS WHERE COMMENTID = %s

This query is used on edit comment.

Update query of comments table:

.. code-block:: sql
	UPDATE COMMENTS SET
                        USERNAME=%s,
			COMMENT=%s,
			ACTIONID=%s
                        WHERE COMMENTID = %s
        
Delete a comment with its comment id query:

.. code-block:: sql
	DELETE FROM COMMENTS WHERE COMMENTID = %s

There is also an option to delete all comments of an action(post), query of that:

.. code-block:: sql
	DELETE FROM COMMENTS WHERE ACTIONID = %s

Get action id of comment query:

.. code-block:: sql
	SELECT ACTIONID FROM COMMENTS WHERE COMMENTID = %s

Reports Table
-----------

Create table query of Reports table:

.. code-block:: sql
	CREATE TABLE IF NOT EXISTS REPORTS
			(
			    ID SERIAL NOT NULL,
			    REPORTTEXT TEXT NOT NULL,
			    COMMENTID INT NOT NULL REFERENCES COMMENTS(COMMENTID) ON DELETE CASCADE,
			    USERNAME TEXT NOT NULL REFERENCES USERS(USERNAME) ON DELETE CASCADE,
			    DATE TIMESTAMP NOT NULL,
			    PRIMARY KEY (id)
			)
Reports table uses references of comments and users table. Comment ID is used for show reported comment. Username is username of reporter. 
Get all query for reports table: 

.. code-block:: sql
SELECT REPORTS.ID, REPORTS.REPORTTEXT, REPORTS.COMMENTID, REPORTS.USERNAME, COMMENTS.COMMENT DATE FROM REPORTS, COMMENTS WHERE ( REPORTS.COMMENTID = COMMENTS.COMMENTID )

Comments table is added since comment text will be printed in reports list page. 

Delete report query

.. code-block:: sql
	DELETE FROM REPORTS WHERE ID = %s

Update report query is not implemented since it is unneeded.

Notifications Table
-----------

Create query of Notifications table:

.. code-block:: sql
	CREATE TABLE IF NOT EXISTS NOTIFICATIONS
			(
			    ID SERIAL NOT NULL,
			    COMMENTID INT NOT NULL REFERENCES COMMENTS(COMMENTID) ON DELETE CASCADE,
			    COMMENTER TEXT NOT NULL REFERENCES USERS(USERNAME) ON DELETE CASCADE,
			    RECEIVER TEXT NOT NULL REFERENCES USERS(USERNAME) ON DELETE CASCADE,
			    DATE TIMESTAMP NOT NULL,
			    ISREAD BOOLEAN NOT NULL,
			    PRIMARY KEY (id)
			)

Notifications table uses references of users and comments table. Commenter is username of comment writer, receiver is username of owner of action(post). 
Insert to Notifications table query:

.. code-block:: sql
	INSERT INTO NOTIFICATIONS
			    (
				COMMENTID, COMMENTER, RECEIVER, DATE)
				VALUES(%s, %s, %s, %s
			    )

Insert to notifications table is done shortly after from insertion to comments table. 

Select notifications query:

.. code-block:: sql
	SELECT USERS.NAME, USERS.SURNAME, COMMENTS.COMMENT, ACTIONID, NOTIFICATIONS.DATE, ISREAD, NOTIFICATIONS.ID, 
		RECEIVER, COMMENTER
		FROM NOTIFICATIONS, COMMENTS, USERS WHERE USERS.USERNAME = COMMENTER AND  COMMENTS.COMMENTID = NOTIFICATIONS.COMMENTID AND RECEIVER != COMMENTER
		    AND RECEIVER = %s
		ORDER BY NOTIFICATIONS.DATE DESC 

Select query is designed to show notifications to user which notifications he/she must is taken. 
Is Read attribute is changed with update queries;
Update one notification’s is read attribute:

.. code-block:: sql
	UPDATE NOTIFICATIONS SET
				ISREAD = true
				WHERE ID = %s

Query of update all notifications of a user:

.. code-block:: sql
	UPDATE NOTIFICATIONS SET
				ISREAD = true
				WHERE RECEIVER = %s
