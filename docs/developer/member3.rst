Parts Implemented by Mahmut Lutfullah Özbilen
=============================================

Actions Table
-------------

Create ACTIONS:

.. code-block:: sql

	CREATE TABLE IF NOT EXISTS ACTIONS
				(
					ACTIONID SERIAL NOT NULL,
					USERNAME TEXT NOT NULL REFERENCES USERS(USERNAME) ON DELETE CASCADE,
					CONTENTID INTEGER NOT NULL REFERENCES CONTENT(ID) ON DELETE CASCADE,
					ACTIONTYPE TEXT,
                    ACTIONCOMMENT TEXT,
                    DATE TIMESTAMP NOT NULL,
                    PRIMARY KEY (ACTIONID))

Create query of ACTION table. ACTIONID is the primary key of the table. USERNAME is the owner user of the action which is also used for reference to USERS table. CONTENTID is the attribute to reference related to CONTENT table. ACTION table is designed for multiple actions like sharing, following, commenting etc. Only commenting action is used in this part of the project. So ACTIONTYPE is holds type of the action. DATE is the date of the action.

Insert into ACTIONS:

.. code-block:: sql

	INSERT INTO ACTIONS
					(
						USERNAME, CONTENTID, ACTIONTYPE, ACTIONCOMMENT, DATE)
						VALUES(%s, %s, %s, %s, %s
						)
						
When user enters a comment insert action query executes and inserts into table.

Select actions query for timeline:

.. code-block:: sql

	SELECT ACTIONS.USERNAME, CONTENTID, ACTIONTYPE, ACTIONCOMMENT, DATE, ACTIONID, NAME, SURNAME, PROFPIC FROM ACTIONS, USERS
                    WHERE (ACTIONS.USERNAME = %s
                    OR ACTIONS.USERNAME IN (SELECT FOLLOWED FROM USERFOLLOW
                                            WHERE FOLLOWER = %s)) AND ACTIONS.USERNAME = USERS.USERNAME
                    ORDER BY 5 DESC
					
When user enters timeline sees the actions of himself/herself or following users. To do so, session username and actions username comparing for actions themselves. Also actions of followings are checking from USERFOLLOW table. Selected tuples are ordering by action date.

Select actions query for content:

.. code-block:: sql
	
	SELECT ACTIONS.USERNAME, CONTENTID, ACTIONTYPE, ACTIONCOMMENT, DATE,NAME,SURNAME,PROFPIC FROM ACTIONS,USERS WHERE (CONTENTID = %s) AND (ACTIONS.USERNAME=USERS.USERNAME) ORDER BY 5 DESC

This query is using to list actions of content. Also checking for whom writes this action.

Edit action query:

.. code-block:: sql

	UPDATE ACTIONS SET ACTIONCOMMENT = %s WHERE ACTIONID = %s

This query is used to update query. Only comment can be updated by user.

Get editing action query:

.. code-block:: sql

	SELECT ACTIONCOMMENT FROM ACTIONS WHERE ACTIONID = %s

To show comment to user before updating.

Delete action query:

.. code-block:: sql

	Delete From ACTIONS
			WHERE ACTIONID = %s
				
Critic Table
------------

Create table query for CRITIC table:

.. code-block:: sql

	CREATE TABLE IF NOT EXISTS CRITIC
				    (
					CRITICID SERIAL NOT NULL,
					NAME TEXT NOT NULL,
                    SURNAME TEXT NOT NULL,
                    WORKPLACE TEXT NULL,
                    PROFPIC TEXT,
                    PRIMARY KEY (CRITICID)
				    )
					
CRITICID is the serial primary key for the CRITIC table. NAME and SURNAME attributes for critic’s name and surname. WORKPLACE is where critic writes his/her review. PROFPIC attribute holds url of the critic’s picture.

Add query for CRITIC table:

.. code-block:: sql

	INSERT INTO CRITIC
					(
						NAME, SURNAME, WORKPLACE,PROFPIC)
						VALUES(%s, %s, %s,%s
						)

Admins can add new critic using sufficient information.

Query to edit CRITIC table:

.. code-block:: sql

	UPDATE CRITIC SET 
                    NAME = %s, 
                    SURNAME = %s,
                    WORKPLACE = %s,
                    PROFPIC = %s
                    WHERE CRITICID = %s
					
Admins can edit selected critic. Query checks it by CRITICID.

Query of deleting CRITIC table:

.. code-block:: sql

	Delete From CRITIC
                WHERE CRITICID = %s
				
Select query for critic’s page:

.. code-block:: sql

	SELECT * FROM CRITIC WHERE CRITICID = %s

This using for show information while editing critic and for the critic’s page.

Select query for listing all critics:

.. code-block:: sql

	SELECT NAME, SURNAME, WORKPLACE, CRITICID, PROFPIC FROM CRITIC

Review Table
------------

Create query for REVIEW table:

.. code-block:: sql

	CREATE TABLE IF NOT EXISTS REVIEW
				(
					REVIEWID SERIAL NOT NULL,
                    CRITICID INTEGER NOT NULL REFERENCES CRITIC(CRITICID) ON DELETE CASCADE,
                    CONTENTID INTEGER NOT NULL REFERENCES CONTENT(ID) ON DELETE CASCADE,
					REVIEW TEXT NOT NULL,
                    DATE TEXT NOT NULL,
                    SCORE INTEGER NOT NULL,
                    PRIMARY KEY (REVIEWID),
                    CHECK ((SCORE >= 0) AND (SCORE <= 100))
				)

REVIEWID is the serial primary key of table. CRITICID attribute holds id of review writer (critic), CONTENTID holds id of the related content. REVIEW is review, DATE is when review is written and SCORE is score of critic.

Insert query:

.. code-block:: sql

	INSERT INTO REVIEW
					(
						CRITICID, CONTENTID, REVIEW, DATE,SCORE)
						VALUES(%s, %s, %s, %s, %s
						)
						
Update query:

.. code-block:: sql

	UPDATE REVIEW SET 
                    CRITICID = %s, 
                    REVIEW = %s,
                    DATE = %s,
                    SCORE = %s
                    WHERE REVIEWID = %s

Delete query:

.. code-block:: sql

	Delete From REVIEW
                WHERE REVIEWID = %s
				
All this operations are done by admin.

Select query for updating review:

.. code-block:: sql

	SELECT * FROM REVIEW WHERE REVIEWID = %s

While updating a review old values can be seen.

Select query for reviews of critic:

.. code-block:: sql

	SELECT REVIEW, REVIEW.DATE,SCORE,ID, TITLE, ARTIST, CONTENTPIC, REVIEWID FROM REVIEW, CONTENT WHERE ((CRITICID = %s) AND (REVIEW.CONTENTID = CONTENT.ID))

This query is to show reviews of critic on critic page.

Select reviews of content:

.. code-block:: sql

	SELECT NAME, SURNAME, WORKPLACE, REVIEW, DATE,SCORE,PROFPIC,REVIEWID,REVIEW.CRITICID FROM REVIEW, CRITIC WHERE ((CONTENTID = %s) AND (REVIEW.CRITICID = CRITIC.CRITICID))

Written reviews about content can be seen by users.

Select query for get metascore:

.. code-block:: sql

	SELECT AVG(SCORE) FROM REVIEW WHERE CONTENTID = %s

Metascore is average value of scores given by critics. Users can see metascore on content’s page.
