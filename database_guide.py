'''
The system uses a MySQL database to store data.
The host, user, password, and database name are hardcoded into the database_manager.py file.
'''

'''
The table names are also hardcoded, they are:
*the `users` table is not automatically created by database_manager. Manual.

users
SCHEMA:
CREATE TABLE `users` (
  `username` varchar(20) NOT NULL,
  `password` varchar(100) NOT NULL,
  `is_logged_in` tinyint NOT NULL,
  PRIMARY KEY (`username`)
)

evnt
SCHEMA:
CREATE TABLE `evnt` (
  `ticket_no` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `course_section` varchar(20) NOT NULL,
  `date` date NOT NULL,
  PRIMARY KEY (`ticket_no`),
  UNIQUE KEY `name` (`name`,`course_section`)
)

evnt_config
SCHEMA:
CREATE TABLE `evnt_config` (
  `name` varchar(50) NOT NULL,
  `venue` varchar(50) NOT NULL,
  `date` varchar(20) NOT NULL,
  `start_time` varchar(20) NOT NULL,
  `end_time` varchar(20) NOT NULL
)
'''

import mysql.connector as mql

def create_users_table():
    conn = mql.connect(
            user = 'root', password='1234',
            host='127.0.0.1',
            database='ticketingsystem'
        )
    cursor = conn.cursor()

    try:
        cursor.execute('''CREATE TABLE users
                       (username VARCHAR(20) PRIMARY KEY,
                       password VARCHAR (100) NOT NULL,
                       is_logged_in TINYINT NOT NULL)''')
        conn.commit()
        print("users table successfully created.")
    except Exception as e:
        conn.rollback()
        print(e)
    finally:        
        conn.close()

def insert_initial_user_data():
    conn = mql.connect(
            user = 'root', password='1234',
            host='127.0.0.1',
            database='ticketingsystem'
        )
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users VALUES ('admin', '1234', 0)")
        conn.commit()
        print("initial data successfully inserted.")
    except Exception as e:
        conn.rollback()
        print(e)
    finally:        
        conn.close()