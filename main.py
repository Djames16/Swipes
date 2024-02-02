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

@app.route('/register', methods=['Get','Post'])
def register():
    if request.method=='POST':
        new_email=request.form["Email"]
        new_username=request.form["Username"]
        new_password=request.form["Password"]
        new_description=request.form["Description"]
        cursor=connect.cursor()
        cursor.execute(f"INSERT INTO `User`(`Username`, `Password`, `Email`, `Description`) VALUES ('{new_username}', '{new_email}', '{new_password}', '{new_description}')")
        cursor.close()
        connect.commit()
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