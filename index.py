from flask import Flask, render_template, request, session
import sqlite3

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret" #TODO encrypt key

dbname = "db-for-secure-web-prac.sqlite3"


@app.route("/index")
def index():
    print "index"
    title = "toppage"
    message = "input your name"
    return render_template("index.html", message=message, title=title)


@app.route("/authorize", methods=["POST"])
def authorize():
    username = request.form["name"]
    password = request.form["password"]
    id = succeedLogin(username, password)
    if request.method == "POST" and id:
        title = "authorize"
        print "name = %s" % username
        session["username"] = username
        session["id"]       = id
        print "id: " + str(session["id"]) + " username: " + session["username"]
        return render_template("authorized.html", title=title, username=username)
    else:
        return "failed login"

@app.route("/mypage", methods=["GET"])
def mypage():
    if session.get("username") is not None:
        if request.method == "GET":
            search = request.args.get("search", "")
            items = searchWord(search)
        return render_template("mypage.html", title="mypage", username=session.get("username"), items=items, search=search)
    else:
        return render_template("mypage.html", title="not authorized")

def succeedLogin(username, password):
    if len(username) is not 0 and len(password) is not 0:
        cnct   = sqlite3.connect(dbname)
        sqlite = cnct.cursor()
        stmt   = "select id, name from user where name=? and password=?"
        sqlite.execute(stmt, (username, password))
        user = sqlite.fetchall()
        print user
        if len(user):
            sqlite.close()
            return user[0][0]
        else:
            return False
        
    else:
        return False

def searchWord(search):
    cnct   = sqlite3.connect(dbname)
    sqlite = cnct.cursor()
    if len(search) is not 0:
        stmt = "select name, value from goods where name=? and user_id=?"
        print "searcher id: " + str(session["id"])
        sqlite.execute(stmt, (search, session["id"]))
        items = sqlite.fetchall()
        return items
    else:
        stmt = "select name, value from goods where user_id=?"
        sqlite.execute(stmt, (session["id"],))
        items = sqlite.fetchall()
        return items

if __name__ == "__main__":
    app.run(host="0.0.0.0")