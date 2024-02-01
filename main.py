from flask import Flask, render_template, request, redirect
import pymysql
from flask_httpauth import HTTPBasicAuth

app=Flask(__name__)
auth = HTTPBasicAuth()
@app.route('/')
def index():
    return render_template(
        "landing.html.jinja"
     )

@app.route('/register')
@auth.login_required
def index():
    if request.method=='POST':
        new_email=request.form["new_user"]
        new_username=request.form["new_user"]
        new_possword=request.form["new_user"]
        cursor=connect.cursor()
        cursor.execute(f"INSERT INTO `User`(`Username`, `Password`, `Email`) VALUES('{new_user}')")
        cursor.close()
        connect.commit()
def register():
    return render_template(
        "Signup.html.jinja"
     )

connect=pymysql.connect(
    database="djames_Swipes",
    user="djames",
    password="228118717",
    host="10.100.33.60",
    cursorclass=pymysql.cursors.DictCursor
)