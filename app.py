
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


def open_specific_database(db_name: str, query: str) -> list:
    database = sqlite3.connect(f"database/{db_name}")
    database.row_factory = sqlite3.Row
    cursor = database.cursor()
    cursor.execute(f"SELECT * FROM {query}")
    return [dict(row) for row in cursor.fetchall()]


@app.route("/")
def index():
    # Home page; Gets its items from database/index.db
    items: list = open_specific_database('index.db', "index_contents")
    return render_template("index.html", items=items)


@app.route('/test')
def test():
    return render_template("test.html")

# TODO: Combine search and search_plain.
# Perhaps use a variable to detirmine which template should be rendered?


@app.route('/search', methods=["POST", "GET"])
def search():
    # For someone to access this route directly, it means we want to load the whole thing
    search_query = request.args.get('q')
    display_plain = request.args.get('plain')
    if search_query is not None and search_query.strip() != '':
        # Get stuff from our databases
        items: list = get_items_from_database()
        # filter based on user search query
        result: list = get_matching_items_from_database(items, search_query)

        # If we came here by searching/clicking on search from navbar, then put the search query on the search box
        if display_plain != "true":
            return render_template("search.html", items=result, override=search_query)
        # If not, we don't need to
        return render_template("search_plain.html", items=result)

    # Fixes a bug where when you remove the query from the search box it re-renders search.html
    elif display_plain == "true":
        return render_template("search_plain.html")

    return render_template("search.html")


def get_items_from_database() -> list:
    # Open database/* and do "select * from ?"
    # Where ? is found under database_select_index.txt
    select_queries: list = []
    with open("database/database_select_index.txt", 'r') as index:
        # For each line, we have filename {space} database
        for line in index:
            # Separate by space
            filename, query, location = line.split(' ')
            database = sqlite3.connect(f"database/{filename}")
            database.row_factory = sqlite3.Row
            cursor = database.cursor()
            cursor.execute(f"SELECT * FROM {query}")
            result = []

            for row in cursor.fetchall():
                test = dict(row)
                test["location"] = f"{location}"
                result.append(test)

            select_queries.append(result)

    return select_queries


def get_matching_items_from_database(items: list, search_query: str):
    result = []
    found = False
    for all_databases in items:
        # If item contains search_query, append
        # Items is a list of a list of a dict still
        for specific_database in all_databases:
            for value in specific_database.values():
                if not found:
                    if search_query.lower() in str(value).lower():
                        # append id
                        found = True
                        result.append({"card_title": specific_database["card_title"],
                                       # [:-5] removes the .html
                                       "location": specific_database["location"][:-5],
                                       "description": specific_database["card_text"]})
                        # TODO: once i append, go to the next database
                else:
                    continue
            found = False
    return result


@app.route('/resources/outlook')
def outlook():
    # Open database
    database = sqlite3.connect("database/outlook_issues.db")
    database.row_factory = sqlite3.Row

    # Get the items and convert them to dict
    cursor = database.cursor()
    cursor.execute("SELECT * FROM issues")
    items = [dict(row) for row in cursor.fetchall()]

    # Render outlook.html with the items from the database
    return render_template("resources/outlook.html", items=list(items))


@app.route('/guides/outlook_authenticator')
def outlook_authenticator():
    return render_template("guides/outlook_authenticator.html")


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404
