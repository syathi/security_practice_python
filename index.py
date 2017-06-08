from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret" #TODO encrypt key

dbname = "db-for-secure-web-prac.sqlite3"


@app.route("/index")
def index():
    print "index"
    title = "toppage"
    return render_template("index.html", title=title)


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

@app.route("/mypage/", methods=["GET"])
def mypage():
    if session.get("username") is not None:
        if request.method == "GET":
            search = request.args.get("search", "")
            items = searchWord(search)
        return render_template("mypage.html", title="mypage", username=session.get("username"), items=items, search=search)
    else:
        return render_template("mypage.html", title="not authorized")

@app.route("/mypage/update", methods=["GET"])
def update():
    if session.get("username") is not None:
        token = session.pop("_csrf_token", None)
        print token
        name  = request.args.get("name", "")
        value = request.args.get("value", "")
        return render_template("update.html", name=name, value=value)
    else:
        return "not authorized"

@app.route("/mypage/create", methods=["POST"])
def create():
    newName  = request.form["newname"]
    newValue = request.form["newvalue"]
    name     = request.form["name"]
    value    = request.form["value"]
    updateData(newName, newValue, name, value)
    return redirect(url_for("mypage", title="mypage", username=session.get("username")))

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

def updateData(newName, newValue, name, value):
    print newName + " " + newValue + " " + name + " " + value
    cnct   = sqlite3.connect(dbname)
    sqlite = cnct.cursor()
    stmt = "update goods set name=? , value=? where name=? and value=?"
    sqlite.execute(stmt, (newName, newValue, name, value))
    cnct.commit()
    sqlite.close()
    cnct.close()

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")