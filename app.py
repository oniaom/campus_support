from flask import Flask, render_template, request, redirect
from sqlite_lib import SQL
import helpers

app = Flask(__name__)

def _debug_print(args):
    import sys
    print(args, file=sys.stderr)

@app.route("/")
def index():
    # Home page; Gets its items from database/index.db
    database: SQL = SQL("database/index.db")

    # Get the index contents table name and query it
    table_name: str = database.get_tables()[0]
    items: list = database.execute(f"SELECT * FROM {table_name}")
    
    return render_template("index.html", items=items)


@app.route('/search', methods=["POST", "GET"])
def search():
    # Handles searching through our database for matching strings.
    # Also gets called by our js for real time results (calls plain=true in args)
    search_query = request.args.get('q')
    display_plain = request.args.get('plain')

    # Assuming that the user searched for something
    if search_query is not None and search_query.strip() != '':
        # TODO: FIXME: this monstrocity.
        # Potentially rewrite the whole search...
        # Won't work for now because i changed get_matching..._database

        # Get stuff from our databases
        items: list = get_items_from_database_with_location()
        # filter based on user search query
        result: list = get_matching_items_from_database(items, search_query)

        # If we came here by searching/clicking on search from navbar, then put the search query on the search box
        # We also want to display the whole page as opposed to just the search results
        if display_plain != "true":
            return render_template("search.html", items=result, override=search_query)

        # If not, we should render the plain version without overriding the search box
        return render_template("search_plain.html", items=result)

    # Fixes a bug where when you remove the query from the search box it re-renders search.html
    elif display_plain == "true":
        return render_template("search_plain.html")

    return render_template("search.html")


def get_items_from_database_with_location() -> list:
    # Open database/* and do "select * from ?"
    # Where ? is found under database_select_index.txt
    select_queries: list = []
    with open("database/database_select_index.txt", 'r') as index:
        # For each line, we have filename {space} database {space} html_location
        for line in index:
            # Separate by space
            filename, table_name, location = line.split(' ')
            # Call our function to open the database
            select_queries.append(
                helpers.get_query_with_location(filename, table_name, location))

    return select_queries


def get_matching_items_from_database(items: list, search_query: str):
    result = []
    found = False
    for all_databases in items:
        # If item contains search_query, append
        # Items is a list of a list of a dict still
        for specific_database in all_databases:
            found = helpers.search_current_database(specific_database, search_query)
            if found:
                result.append({"card_title": specific_database["card_title"],
                               "location": specific_database["location"],
                               "description": specific_database["card_text"]})
    return result


@app.route('/resources/outlook')
def outlook():
    # Open database
    db = SQL("database/outlook_issues.db")
    items = db.execute("SELECT * FROM issues")
    
    # Render outlook.html with the items from the database
    return render_template("resources/outlook.html", items=items)


@app.route('/guides/outlook_authenticator')
def outlook_authenticator():
    return render_template("guides/outlook_authenticator.html")


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404
