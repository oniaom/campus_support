import sqlite3

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


def search_current_database(specific_database: dict, search_query: str) -> bool:
    """ Searches database rows (result) if it contains a specific query """
    # TODO: just get a db name and open it from here. Right now it relies on values already obtained
    for value in specific_database.values():
        if search_query.lower() in str(value).lower():
            return True
    return False


def get_query_with_location(filename: str, query: str, location: str) -> list:
    result = open_specific_database(filename, query)
    for item in result:
        item["location"] = f"{location}"
    return result
