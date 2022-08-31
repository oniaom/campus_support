import sqlite3


class SQL:
    def __init__(self, dbname: str) -> None:
        self.dbname = dbname

        # Open database
        self.database = sqlite3.connect(dbname)
        self.database.row_factory = sqlite3.Row
        self.db_cursor = self.database.cursor()

    def execute(self, query: str) -> list:
        # Returns the result of executing the query from sqlite3 as a list

        # Execute the query
        self.db_cursor.execute(query)

        # Return the result
        return [dict(row) for row in self.db_cursor.fetchall()]
