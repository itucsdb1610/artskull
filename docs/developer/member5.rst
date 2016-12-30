Parts Implemented by Doğay Kamar
================================
Actor Table
-----------
Create query for Actors Table:

.. code-block:: sql
	
	CREATE TABLE IF NOT EXISTS Actors
                    (
                        ActorID SERIAL NOT NULL,
                        NAME TEXT NOT NULL,
                        SURNAME TEXT NOT NULL,
                        BIRTHDAY TEXT NOT NULL,
                        PRIMARY KEY (ActorID)
                    )

					
Name, Surname and Birthday are the personal details of each actor. ActorID is to make every actor in the table unique, so that operations can be done on a single element. 


Insert query for Actors Table:
.. code-block:: sql

	INSERT INTO Actors
                    (
                        NAME, SURNAME, BIRTHDAY)
                        VALUES (%s, %s, %s
                    )
                    
All of the information are given by admin, and insertion is done with every information provided.

Delete query for Actors Table:
.. code-block:: sql

	DELETE FROM Actors
        	WHERE ActorID = %s
        
Delete operation is done with ActorID as deleting is done through a webpage that lists actors, with delete request, ActorID is sent and specific single actor can be deleted.

Update query for Actors Table:
.. code-block:: sql

	UPDATE Actors SET
                        NAME = %s,
                        SURNAME = %s,
                        BIRTHDAY = %s
                        WHERE ActorID = %s
                        
Every attribute of an actor is updated, and update operation is only done on a single actor.

Select query for searching:
.. code-block:: sql

	SELECT NAME, SURNAME, BIRTHDAY, ActorID FROM Actors
                    WHERE NAME = %s OR SURNAME = %s
                    
Given string is searched in name OR surname of an actor and returned.

Select query for all:
.. code-block:: sql

	SELECT NAME, SURNAME, BIRTHDAY, ActorID FROM Actors
  
All actors in the table are returned, this is used when listing all actors in Cast edit or Actor operations page.
Cast Table
----------
Create query for Cast Table:
.. code-block:: sql

	CREATE TABLE IF NOT EXISTS CASTING
                    (
                        ActorID INTEGER NOT NULL REFERENCES Actors(ActorID) ON DELETE CASCADE,
                        ContentID INTEGER NOT NULL REFERENCES CONTENT(ID) ON DELETE CASCADE,
                        ORD INTEGER NOT NULL,
                        PRIMARY KEY(ActorID, ContentID)
                    )
                    
Cast table holds the ActorID referenced from Actors table and ContentID referenced from Content table, which makes a relation that an Actor is in the cast of the given content. When Actor or Content is deleted, every row that contains one of both will be deleted. ORD is the order of the actor in that content. Each actor can participate in a content once, so (ActorID, ContentID) is our primary key.

Insert query for Cast Table:
.. code-block:: sql

	INSERT INTO CASTING
                            (
                                ActorID, ContentID, ORD)
                                VALUES (%s, %s, %s
                            )
                            
Given actor is inserted into the cast of the given content. This operation can only be done by admins.

Delete query for Cast Table:
.. code-block:: sql

	DELETE FROM CASTING
        	WHERE ActorID = %s AND ContentID = %s
        
This query is used when a certain Actor is removed from the cast of a Content.

Update order query for Cast Table:
.. code-block:: sql

	UPDATE CASTING SET
                        ORD = %s
                        WHERE ActorID = %s AND ContentID = %s
Order of a Actor in a cast is updated.

Select query for Cast Table:
.. code-block:: sql

	SELECT NAME, SURNAME, BIRTHDAY, Actors.ActorID, ORD FROM Actors, CASTING
                    WHERE (ContentID = %s AND Actors.ActorID = CASTING.ActorID)
                    ORDER BY ORD ASC
                    
This query is used when listing the cast of a specific content. Actors in the cast are ordered by their order, starring actors are listed first.
Rating Table
------------
Create query for Rating Table:

.. code-block:: sql

	CREATE TABLE IF NOT EXISTS RATING
                    (
                        Username TEXT NOT NULL REFERENCES USERS(USERNAME) ON DELETE CASCADE,
                        ContentID INTEGER NOT NULL REFERENCES CONTENT(ID) ON DELETE CASCADE,
                        Rate INTEGER NOT NULL,
                        PRIMARY KEY(Username, ContentID)
                    )
                    
Each user can have a single vote on each Content, so (Username, ContentID) is the primary key. Rate attribute is the rate user gives for a specific content pointed by ContentID.

Insert query for Rating Table:
.. code-block:: sql

	INSERT INTO RATING
                            (
                                Username, ContentID, Rate)
                                VALUES (%s, %s, %s
                            )
                            
When a user votes for a content that they are yet to vote, their rating is inserted as a new vote in the table.
Delete query for Rating Table:
.. code-block:: sql

	DELETE FROM RATING
        	WHERE Username = %s AND ContentID = %s
        
A vote of a user for a specific content is deleted. 

Update query for Rating Table:
.. code-block:: sql

	UPDATE RATING SET
                        Rate = %s
                        WHERE Username = %s AND ContentID = %s
                        
Update query is called if a user has already voted for a content and they vote for that content again. In that case, their vote is updated with their new given rating.

Checking if a user has voted:
.. code-block:: sql

	SELECT COUNT(*) FROM RATING
                        WHERE (Username = %s AND ContentID = %s)
                        
Since the primary key is (Username, ContentID), this query can only return 1 or 0, and depending on the output, the function that executes this query returns true or false. If returned true, given user has voted for the content pointed by ContentID, otherwise they have not voted for that content yet.

Count query for votes of a content:
.. code-block:: sql

	SELECT COUNT(*) FROM RATING
                        WHERE ContentID = %s
                        
This query counts the votes of a content pointed by ContentID.

Select query for ratings of a content:
.. code-block:: sql

	SELECT Rate FROM RATING
                        WHERE ContentID = %s
                        
This query returns all votes for the content pointed by ContentID. Average rating is calculated with the returned values.

Select query for a single rating:
.. code-block:: sql

	SELECT Rate FROM RATING
                        WHERE (Username = %s AND ContentID = %s)
                        
If the user has already voted for a content, they are informed of the rating they give for the content when they visited the content page. This query returns a user’s vote for a content pointed by ContentID and used for this purpose.
