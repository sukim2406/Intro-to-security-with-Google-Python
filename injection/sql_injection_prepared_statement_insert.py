from re import search
from flask import Flask, render_template, request
import pyodbc

def get_cursor():
    server = "localhost"
    database = "mytest"
    username = "pyuser"
    password = "Test1234%^&"

    mssql_conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER=' + server + '; PORT=1433; DATABASE=' + database + '; UID=' + username + '; PWD=' + password)

    cursor = mssql_conn.cursor()
    return cursor

cursor = get_cursor()

app = Flask(__name__)

@app.route("/item_search", methods=["GET", "POST"])
def item_search():
    search_test = ""

    if request.method == "POST":
        search_text = request.form["searchText"]
    
    search_sql = "insert into escape_test values(?)"

    if search_text:
        cursor.execute(search_sql, search_text)
        result_rows = [["inserted", search_text, "", "", "", ""]]
    else:
        result_rows = [["nothing happening", "", "", "", "", ""]]

    return render_template("sql_injection.html", rows=result_rows, search_text=search_text, sql_quary=search_sql)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)