import sqlite3

from sqlite_lib import SQL


def open_specific_database(db_name: str, query: str) -> list:
    """ Opens a database and returns the result of 'SELECT * FROM table_name (query)' """
    # Open database
    database = sqlite3.connect(f"database/{db_name}")
    database.row_factory = sqlite3.Row

    # Get the items and convert them to dict
    cursor = database.cursor()
    cursor.execute(f"SELECT * FROM {query}")

    # Return the result
    return [dict(row) for row in cursor.fetchall()]

def search_current_database(dbname: str, search_query: str) -> bool:
    # Searches database for keywords
    db = SQL(dbname)
    # Get database tables
    db_tables: list = db.get_tables()
    for table in db_tables:
        exists = db.execute(f"SELECT * FROM {table} WHERE keywords LIKE '%{search_query}%'")
        if exists != []:
            return True
    return False


def search_current_database1(specific_database: dict, search_query: str) -> bool:
    """ Searches database rows (result) if it contains a specific query """
    # TODO: just get a db name and open it from here. Right now it relies on values already obtained
    for value in specific_database.values():
        if search_query.lower() in str(value).lower():
            return True
    return False


def get_query_with_location(filename: str, table_name: str, location: str) -> list:
    db = SQL(filename)
    result = db.execute(f"SELECT * FROM {table_name}")
    for item in result:
        item["location"] = location
    return result