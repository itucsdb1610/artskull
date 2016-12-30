Parts Implemented by Furkan Özçelik
===================================
Contents Table
-----------
Create table query for CONTENT table:

.. code-block:: sql
  
  CREATE TABLE IF NOT EXISTS CONTENT
           (
               ID SERIAL NOT NULL,
               TITLE TEXT NOT NULL,
               ARTIST TEXT NOT NULL,
               DURATION TEXT NOT NULL,
               DATE TEXT NOT NULL,
               GENRES TEXT,
               CONTENTPIC TEXT,
               PRIMARY KEY (id)
            )

Create table query is called at very first opening page when there is no content exists. It creates the table “Content” where the data of contents are stored.

.. code-block:: sql

  INSERT INTO CONTENT
           (
               TITLE,ARTIST,DURATION,DATE,GENRES,CONTENTPIC)
               VALUES (%s, %s, %s, %s, %s,%s
            )
           
Insert query is called when new content is added to “Content” table by admin in admin operations section. It automatically assigns an ID to new inserted row.

.. code-block:: sql

  UPDATE CONTENT SET
               TITLE = %s,
               ARTIST = %s,
               DURATION = %s,
               DATE = %s,
               CONTENTPIC = %s,
               GENRES = %s
               WHERE ID = %s
               
Update query is called when admin edits a content. It matches existing content by id in database operations but admins don’t have to deal with id numbers.

.. code-block:: sql
  DELETE FROM CONTENT WHERE ID = %s
  
Delete query is called when admin confirms delete operation of a content. It matches existing content by id in database operations.

Stages Table
-----------
.. code-block:: sql

  CREATE TABLE IF NOT EXISTS STAGE
                   (
                       STAGEID SERIAL NOT NULL,
                       NAME TEXT NOT NULL,
                        LOCATION TEXT NOT NULL,
                     CAPACITY TEXT NOT NULL,
                       STAGEPIC TEXT NOT NULL,
                        PRIMARY KEY (STAGEID)
                   )

Create table query is called at very first opening page when there is no stage exists. It creates the table “Stage” where the data of stages are stored.

.. code-block:: sql
  
  INSERT INTO STAGE
          (
               NAME,LOCATION,CAPACITY,STAGEPIC)
                 VALUES (%s, %s, %s, %s
            )

Insert query is called when new stage is added to “Stage” table by admin in admin operations section. It automatically assigns an STAGEID to new inserted row.

.. code-block:: sql
  
  UPDATE STAGE SET
                   NAME = %s,
                   LOCATION = %s,
                   CAPACITY = %s,
                   STAGEPIC = %s
                   WHERE STAGEID = %s

Update query is called when admin edits a stage. It matches existing stage by stageid in database operations but admins don’t have to deal with id numbers.

.. code-block:: sql
  DELETE FROM STAGE WHERE STAGEID = %s
  
Delete query is called when admin confirms delete operation of a stage. It matches existing stage by stageid in database operations.


Plays Table
-----------

.. code-block:: sql

  CREATE TABLE IF NOT EXISTS PLAY
                    (
                           STAGEID INTEGER REFERENCES STAGE(STAGEID)
                           ON DELETE CASCADE
                           ON UPDATE CASCADE,
                           CONTENTID INTEGER REFERENCES CONTENT(ID)
                           ON DELETE CASCADE
                           ON UPDATE CASCADE,
                           DATE TEXT NOT NULL,
                            PRIMARY KEY (STAGEID,CONTENTID)
                     )
                     
Create table query is called at very first opening page when there is no play exists. It creates the table “Play” where the data of plays are stored. Play table references from content and stage table.  


.. code-block:: sql
  
  INSERT INTO PLAY
              (
                   STAGEID,CONTENTID,DATE)
                     VALUES (%s, %s, %s
                )

Insert query is called when admin adds a new play by combine of stage, content and date.


.. code-block:: sql
  
  UPDATE PLAY SET
                   STAGEID = %s,
                   CONTENTID = %s,
                   DATE = %s
                   WHERE (STAGEID = %s) AND (CONTENTID = %s)

Update query is called when admin edits an existing play. It matches play from both stageid and contentid.

.. code-block:: sql

  DELETE FROM PLAY WHERE (STAGEID = %s) AND (CONTENTID = %s)
  
Delete query is called when admin deletes an existing play. It matches play from both stageid and contentid.
