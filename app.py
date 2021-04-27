from flask import Flask, render_template, request, redirect
import shortuuid
import markdown
import mysql.connector

app = Flask(__name__)

mydb = mysql.connector.connect(
    host="localhost", user="root", password="", database="python"
)


@app.route("/")
def homepage():
    return render_template("home.html")


@app.route("/create", methods=["GET", "POST"])
def createPage():

    content = request.form["content"]
    urlCustom = request.form["urlCustom"]

    if urlCustom == "":
        url = shortuuid.ShortUUID().random(length=6)
    elif len(urlCustom) < 6:
        url = urlCustom.replace(" ", "") + "—" + shortuuid.ShortUUID().random(length=6)
    else:
        url = shortuuid.ShortUUID().random(length=6)

    cur = mydb.cursor()
    s = """INSERT INTO data (content, url) VALUES('%s', '%s') """ % (content, url)
    cur.execute(s)
    mydb.commit()

    return redirect("/articles/" + url, code=302)


@app.route("/articles/<url>", methods=["GET", "POST"])
def articles(url):

    cur = mydb.cursor()
    s = """SELECT * FROM data WHERE url = '%s'""" % (url)
    cur.execute(s)
    data = cur.fetchone()

    if data:
        return render_template(
            "get.html", text=data, content=markdown.markdown(data[1])
        )
    else:
        return render_template("notFound.html")


@app.route("/articles/admin", methods=["GET", "POST"])
def articlesAdmin():

    cur = mydb.cursor()
    s = """SELECT * FROM data"""
    cur.execute(s)
    data = cur.fetchall()

    return render_template("admin.html", text=data)


@app.route("/articles/admin/delete/<article_id>", methods=["POST", "GET"])
def articlesDeleteAdmin(article_id):

    cur = mydb.cursor()
    s = """DELETE FROM data WHERE id = %s""" % (article_id)
    cur.execute(s)
    return redirect("/articles/admin", code=302)


@app.route("/articles/admin/<url>", methods=["GET", "POST"])
def articlesUpdateAdminInterface(url):

    cur = mydb.cursor()
    s = """SELECT * FROM data WHERE url = '%s'""" % (url)
    cur.execute(s)
    data = cur.fetchone()

    if data:
        return render_template(
            "update.html", text=data, content=markdown.markdown(data[1])
        )
    else:
        return render_template("notFound.html")


@app.route("/articles/admin/update/<article_id>", methods=["GET", "POST"])
def articlesUpdateAdmin(article_id):
    content = request.form["content"]
    cur = mydb.cursor()
    s = """UPDATE `data` SET `content`= '%s' WHERE id = %s""" % (content, article_id)
    cur.execute(s)
    return redirect("/articles/admin", code=302)
