import sqlite3

############ CREATING A DB AND CONNECTING #################
def connect_to_sql():
    """ Crea la base de datos y crea la tabla - en caso de no existir.

    Args:
        none

    Returns:
        none
    """


    try:

        sqliteConnection = sqlite3.connect('ticket.db')
        cursor = sqliteConnection.cursor()
        if __name__ == "__main__":
            print("Database created and Successfully Connected to SQLite")
        cursor.close()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite.Error: ", error)

    finally:
        if sqliteConnection:
            sqliteConnection.close()
            if __name__ == "__main__":
                print("The SQLite connection is closed")


    ############ CREATING A TABLE #################


    try:

        sqliteConnection = sqlite3.connect('ticket.db')

        sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS ticket_table (
                                    id INTEGER PRIMARY KEY,
                                    ticker_symbol TEXT,
                                    ticker_date datetime,
                                    close_value REAL);'''

        cursor = sqliteConnection.cursor()
        if __name__ == "__main__":
            print("Successfully Connected to SQLite")
        cursor.execute(sqlite_create_table_query)
        sqliteConnection.commit()
        if __name__ == "__main__":
            print("SQLite table created")
        cursor.close()

    except sqlite3.Error as error:
            print("Error while creating a sqlite table.Error: ", error)
    finally:
            if sqliteConnection:
                sqliteConnection.close()
                if __name__ == "__main__":
                    print("sqlite connection is closed")


