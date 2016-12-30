Parts Implemented by Muhammed Kadir Yücel
=========================================
Users Table
-----------
Create table query for USERS table:

.. code-block:: sql
	CREATE TABLE IF NOT EXISTS USERS
                    (
                        USERNAME TEXT UNIQUE NOT NULL,
                        SALT TEXT NOT NULL,
                        HASH TEXT NOT NULL, 
                        EMAIL TEXT UNIQUE NOT NULL,
                        NAME TEXT NOT NULL,
                        SURNAME TEXT NOT NULL,
                        PROFPIC TEXT,
                        PRIMARY KEY (USERNAME)
                    );
					
You can see that password is not hold as plain text in the table. There are two attributes named as “SALT” and “HASH” that takes place for password. When user enters a password at sign up page, a random string, called as salt, will be added end of the user entered password. Then this resulting text will be hashed and stored in the table with created salt. Code can be found in “user.py” file that contains definition of User class:

.. code-block:: python

	def createSalt():
    ABECE = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    chars = []
    for i in range(16):
        chars.append(random.choice(ABECE))

    real_salt = "".join(chars)
    return real_salt

	def createHash(salt, passwd):
		salted_password = passwd.join(salt)
		h = hashlib.md5(salted_password.encode())
		#print(h.hexdigest())
		return h.hexdigest()
		
Then resulting object of User class will be directed to the method that will add the user to the USERS table:

.. code-block:: sql

	INSERT INTO USERS
                 (
                   USERNAME, SALT, HASH, EMAIL, NAME, SURNAME, PROFPIC)
                   VALUES (%s, %s, %s, %s, %s, %s, %s
                 );
				 
When user wants to update him/her informations, there are two specific queries. If user wanted to change him/her password the following query will work since newly created salt and hash values should be set:

.. code-block:: sql

	UPDATE USERS SET 
                    NAME = %s,
                    SURNAME = %s,
                    EMAIL = %s,
                    SALT = %s,
                    HASH = %s,
                    PROFPIC = %s
                    WHERE USERNAME = %s	

If user leaved password field empty on user edit page, new salt and hash values would not be generated and so the following query can get job done easily:

.. code-block:: sql

	UPDATE USERS SET 
                    NAME = %s,
                    SURNAME = %s,
                    EMAIL = %s,
                    PROFPIC = %s
                    WHERE USERNAME = %s
					
If user clicked “Delete account” button on his/her profile edit page, the user information will be deleted from USERS table permenantly:

.. code-block:: sql
	
	DELETE FROM USERS WHERE USERNAME = %s
	
Only username information will be enough since it is the primary key for the USERS table.
When you are searching for users from the search box on the top-menu bar, the following query works and your input will be searched in USERS table for users’ names, surnames, usernames and emails:

.. code-block:: sql

	SELECT USERNAME, EMAIL, NAME, SURNAME, PROFPIC FROM USERS WHERE ( (LOWER(USERNAME) LIKE LOWER(%s)) OR
                    (LOWER(EMAIL) LIKE LOWER(%s)) OR (LOWER(NAME) LIKE LOWER(%s) ) OR (LOWER(SURNAME) LIKE LOWER(%s))) ORDER BY NAME
					
We have used “LOWER” operation to make results all lower case, this will not affect the results that will be showed on the search results page and original data in the table. Result will be ordered by users’ real names.

Admins Table
------------
Create table query for ADMINS table:

.. code-block:: sql

	CREATE TABLE IF NOT EXISTS ADMINS
                (
                    ADMINUSERNAME TEXT NOT NULL REFERENCES USERS(USERNAME) ON DELETE CASCADE ON UPDATE CASCADE,
                    ADMINORDER INTEGER NOT NULL,
                    PRIMARY KEY(ADMINUSERNAME, ADMINORDER)
                )
				
With this table structure, ADMINUSERNAME attribute is references USERNAME attribute in USERS table. So if there is no tuple with given username in USERS table, admin will not be added. Also, if the admin user is deleted from USERS table(system), also its privileges will be deleted, i.e. its admin rights will be deleted to prevent new registrations with same usernames to unauthorized access.

Following Mechanism
-------------------
Create table query for FOLLOWINGS table:

.. code-block:: sql

	CREATE TABLE IF NOT EXISTS USERFOLLOW
                    (
                        FOLLOWER TEXT NOT NULL REFERENCES USERS(USERNAME) ON DELETE CASCADE,
                        FOLLOWED TEXT NOT NULL REFERENCES USERS(USERNAME) ON DELETE CASCADE,
                        FOLLOWDATE TIMESTAMP NOT NULL,
                        PRIMARY KEY(FOLLOWER, FOLLOWED)
                    )
					
This table holds following user and followed user with their usernames and the current date that user started to follow.
When you enter a user’s profile or your profile, you can see number of people that you are following and number of people that are following you. By using “COUNT” operation we could gain that feature in Artskull:

.. code-block:: sql

	SELECT COUNT(FOLLOWER) FROM USERFOLLOW WHERE FOLLOWED = %s
