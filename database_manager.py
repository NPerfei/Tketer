import mysql.connector as mql

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.cursor = None

        self.initialize_tables()
    
    def get_connection(self):
        try:
            self.connection = mql.connect(
            user = 'root', password='1234',
            host='127.0.0.1',
            database='ticketingsystem'
            )
            self.cursor = self.connection.cursor()
            print("Connection established successfully.")
        except mql.Error as e:
            print("Error connecting to databese:", e)

    def close_connection(self):
        if self.cursor:
            self.cursor.close()
            self.cursor = None
        if self.connection:
            self.connection.close()
            self.connection = None
        print("Connection Closed.")

    def initialize_tables(self): # needs to be modified to have a parameter
        self.get_connection()
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS evnt
                                (ticket_no INT PRIMARY KEY AUTO_INCREMENT,
                                name VARCHAR(50) NOT NULL, 
                                course_section VARCHAR(20) NOT NULL,
                                date DATE NOT NULL,
                                UNIQUE(name, course_section))''')
            
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS evnt_config
                                (name VARCHAR(50) NOT NULL,
                                venue VARCHAR(50) NOT NULL,
                                date VARCHAR(20) NOT NULL,
                                start_time VARCHAR(20) NOT NULL,
                                end_time VARCHAR(20) NOT NULL)''')
            
            print("Tables initialized.")
        except mql.Error as e:
            print(f"Error in creating database: {e}")
        self.close_connection()

    def add_ticket_entry(self, name: str, course_section: str, date: str):
        self.get_connection()

        try:
            query = "INSERT INTO evnt (name, course_section, date) VALUES (%s, %s, %s)"
            data = (name, course_section, date)

            self.cursor.execute(query, data)
            self.connection.commit()

            print("INSERT operation successful.")
        except mql.IntegrityError as e:
            self.connection.rollback()
            raise # to be caught by main
        except mql.Error as e:
            self.connection.rollback()
            print("An error occured while adding data:", e)

        self.close_connection()

    def delete_ticket_entry(self, ticket_number: int):
        self.get_connection()

        try:
            query = "DELETE FROM evnt WHERE ticket_no = (%s)"
            data = (ticket_number,)

            self.cursor.execute(query, data)
            self.connection.commit()

            print("DELETE operation successful.")
        except mql.Error as e:
            self.connection.rollback()
            print("An error has occured while deleting data:", e)

        self.close_connection()

    def update_ticket_entry(self, ticket_number: int, n_name: str, n_course_section: str, n_date: str):
        self.get_connection()

        try:
            query = "UPDATE evnt SET name = %s, course_section = %s, date = %s WHERE ticket_no = %s"
            data = (n_name, n_course_section, n_date, ticket_number)

            self.cursor.execute(query, data)
            self.connection.commit()

            print("UPDATE operation successful.")
        except mql.Error as e:
            self.connection.rollback()
            print("An error has occured while updating data:", e)
        finally:
            self.close_connection()

    def get_data(self, filter: str = None, search: str = None):
        self.get_connection()
        results = None

        try:
            if not filter and not search:
                query = "SELECT * FROM evnt ORDER BY ticket_no ASC"
                self.cursor.execute(query)
            elif not search:
                query = f"SELECT * from evnt ORDER BY {filter} ASC, name asc"
                self.cursor.execute(query)
            else:
                partial_search_pattern = f"%{search}%"
                query = f'''Select * from evnt WHERE {filter} LIKE %s ORDER BY 
                            CASE WHEN {filter} = %s THEN 1 
                            WHEN {filter} LIKE %s THEN 2
                            END, 
                            {filter} ASC'''
                data = (partial_search_pattern, search, partial_search_pattern)
                self.cursor.execute(query, data)

            results = self.cursor.fetchall()
        except mql.Error as e:
            self.connection.rollback()
            print("An error has occurred while fetching data:", e)
        finally:
            self.close_connection()
        
        return results if results else None
    
    def get_datum(self, ticket_number: str):
        self.get_connection()
        result = None

        try:
            query = "SELECT * from evnt WHERE ticket_no = %s"
            data = (ticket_number,)

            self.cursor.execute(query, data)

            result = self.cursor.fetchone()
        except mql.Error as e:
            self.connection.rollback()
            print("An error has occurred while fetching datum:", e)
        finally:
            self.close_connection()
        
        return result if result else None
    
    def delete_multiple(self, option, date=None):
        self.get_connection()
        
        try:
            if option == 1:
                self.cursor.execute("SELECT ticket_no FROM evnt WHERE date > %s", (date,))
                to_delete = self.cursor.fetchall()
                to_delete = [row[0] for row in to_delete]
                if to_delete:
                    placeholders = ", ".join(['%s'] * len(to_delete))
                    query = f"DELETE FROM evnt WHERE ticket_no in ({placeholders})"

                    self.cursor.execute(query, to_delete)
            elif option == 2:
                self.cursor.execute("TRUNCATE TABLE evnt")
            self.connection.commit()
            print("Multiple DELETE operation successful.")
        except mql.Error as e:
            self.connection.rollback()
            print("An error has occured while deleting data:", e)
        finally:
            self.close_connection()

    # login
    def get_admin_credentials(self):
        self.get_connection()

        try:
            self.cursor.execute("SELECT * FROM users")
            credentials = self.cursor.fetchone()[:2]

            return credentials
        except mql.Error as e:
            print("An error has occured while obtaining credentials:", e)
        finally:
            self.close_connection()

    def is_logged_in(self):
        self.get_connection()

        try:
            self.cursor.execute("SELECT is_logged_in FROM users")
            
            return self.cursor.fetchone()
        except mql.Error as e:
            print("An error occured while getting login data:", e)
        finally:
            self.connection.close()

    def log_in_out(self, n):
        self.get_connection()

        try:
            state = (n,)
            query = "UPDATE users SET is_logged_in = %s WHERE username = 'admin'"

            self.cursor.execute(query, state)
            self.connection.commit()
        except mql.Error as e:
            self.connection.rollback()
            print("An error has occured whilw logging in/out:", e)
        finally:
            self.close_connection()
    
    # startup of main
    def get_evnt_config(self):
        self.get_connection()

        try:
            self.cursor.execute('SELECT * from evnt_config')
            event_config = self.cursor.fetchone()

            if event_config:
                return event_config
            else:
                return None #redundant, for clarity only

        except mql.Error as e:
            print("An error has occured while fetching event config data:", e)
            return None
        finally:
            self.close_connection()

    def set_evnt_config(self, name, venue, date, start_time, end_time):
        self.get_connection()

        try:
            self.cursor.execute("DELETE from evnt_config")
            
            data = (name, venue, date, start_time, end_time)
            query = "INSERT INTO evnt_config VALUES (%s, %s, %s, %s, %s)"

            self.cursor.execute(query, data)
            self.connection.commit()
            print("Event Configuration set successfully.")
        except mql.Error as e:
            self.connection.rollback()
            print("An error occured while setting event config:", e)
        finally:
            self.close_connection()
    
    def delete_evnt_config(self):
        self.get_connection()
        
        try:
            self.cursor.execute("DELETE FROM evnt_config")
            self.connection.commit()
        except mql.Error as e:
            self.connection.rollback()
            print("An error occured while deleting event configurations:", e)
        finally:
            self.close_connection()



# x = DatabaseManager()

# dummy_data = [
#     [
#         "Miguel T. Vargas", "Marisol N. Reyes", "Elena C. Rivera", "Luis S. Garcia",
#         "Ramon N. Martinez", "Rosa S. Lopez", "Miguel E. Gutierrez", "Francisco P. Rodriguez",
#         "Francisco K. Valdez", "Marisol S. Garcia", "Ramon D. Reyes", "Pedro M. Cruz",
#         "Lourdes U. Diaz", "Lourdes M. Torres", "Rosa C. Valdez", "Carlos W. Bautista",
#         "Pedro S. Torres", "Vicente G. Rodriguez", "Carlos H. Morales", "Teresa H. Castro",
#         "Carmen Q. Flores", "Francisco B. Gutierrez", "Juan I. Valdez", "Miguel F. Lopez",
#         "Gloria S. Garcia", "Luis U. Hernandez", "Manuel O. Garcia", "Ana O. Ramos",
#         "Elena F. Santos", "Vicente A. Cruz", "Ramon C. Morales", "Juan L. Valdez",
#         "Lourdes E. Ramos", "Ana R. Rivera", "Jose W. Bautista", "Marisol W. Hernandez",
#         "Ana U. Lopez", "Isabel B. Lopez", "Gloria Y. Castro", "Jose T. Martinez"
#     ],

#     [
#         "BSCE - 3C", "BSEE - 3B", "BSEE - 3B", "BSED - 1B", "BSEE - 1B", 
#         "BSIT - 2B", "BSCE - 1C", "BSED - 2A", "BSCE - 2A", "BSEE - 3B", 
#         "BSEE - 4C", "BSEE - 3B", "BSIT - 4B", "BSED - 1A", "BSED - 1A", 
#         "BSIT - 4A", "BSED - 4C", "BSED - 3C", "BSCE - 1A", "BSED - 3B",
#         "BSCE - 3B", "BSIT - 3A", "BSEE - 2A", "BSEE - 1A", "BSEE - 1A", 
#         "BSIT - 2A", "BSIT - 4C", "BSED - 2A", "BSEE - 1B", "BSEE - 4A", 
#         "BSEE - 2B", "BSCE - 1B", "BSIT - 3A", "BSEE - 3A", "BSEE - 3A", 
#         "BSIT - 1C", "BSCE - 1B", "BSEE - 3A", "BSEE - 1A", "BSCE - 1C"
#     ],

#     [
#         "2024-11-15", "2024-11-15", "2024-11-19", "2024-11-20", "2024-11-22", 
#         "2024-11-19", "2024-11-25", "2024-11-20", "2024-11-19", "2024-11-21", 
#         "2024-11-19", "2024-11-22", "2024-11-20", "2024-11-20", "2024-11-19", 
#         "2024-11-25", "2024-11-24", "2024-11-20", "2024-11-21", "2024-11-18", 
#         "2024-11-24", "2024-11-25", "2024-11-24", "2024-11-21", "2024-11-19", 
#         "2024-11-24", "2024-11-19", "2024-11-15", "2024-11-24", "2024-11-24", 
#         "2024-11-19", "2024-11-19", "2024-11-23", "2024-11-22", "2024-11-21", 
#         "2024-11-19", "2024-11-24", "2024-11-25", "2024-11-16", "2024-11-18", 
#         "2024-11-24", "2024-11-20", "2024-11-15", "2024-11-17", "2024-11-21", 
#         "2024-11-24", "2024-11-18", "2024-11-24", "2024-11-24", "2024-11-20", 
#         "2024-11-20", "2024-11-20", "2024-11-24", "2024-11-19", "2024-11-24", 
#         "2024-11-18", "2024-11-24", "2024-11-24", "2024-11-23", "2024-11-20"
#     ]
# ]
# for i in range(40):
#     x.add_ticket_entry(dummy_data[0][i], dummy_data[1][i], dummy_data[2][i])