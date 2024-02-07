from flask import Flask, render_template, request, redirect
import pymysql
from flask_httpauth import HTTPBasicAuth
import flask_login

app=Flask(__name__)
auth = HTTPBasicAuth()
app.secret_key="something_secret" #change this
login_manager=flask_login.LoginManager()
login_manager.init_app(app)
class User:
    is_authenticated=True
    is_anonymous=False
    is_active=True
    def __init__(self,id,Username):
        self.Username=Username
        self.id=id
    def get_id(self):
        return str(self.id)
@login_manager.user_loader
def load_user(user_id):
    cursor=connect.cursor()
    cursor.execute("Select * FROM `User` WHERE `id` =" + str(user_id))
    result=cursor.fetchone()
    cursor.close()
    connect.commit()
    if result is None:
        return None
    return User(result["id"], result["Username"])

@app.route('/')
def index():
    return render_template(
        "landing.html.jinja"
     )

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        new_username=request.form["Username"]
        new_password=request.form["Password"]
        new_email=request.form["Email"]
        new_description=request.form["Description"]
        cursor=connect.cursor()
        cursor.execute(f"INSERT INTO `User`(`Username`, `Password`, `Email`, `Description`) VALUES ('{new_username}', '{new_password}','{new_email}', '{new_description}')")
        cursor.close()
        connect.commit()
    return render_template(
        "Signup.html.jinja"
     )

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        Username=request.form["Username"]
        Password=request.form["Password"]
        cursor=connect.cursor()
        cursor.execute(f"Select * FROM `User` WHERE `Username` = '{Username}'")
        result=cursor.fetchone()
        cursor.close()
        connect.commit()
        if Password==result["Password"]:
            User=load_user(result['id'])
            flask_login.login_user(User)
            return redirect('/feed')
        
    return render_template(
        "Login.html.jinja"
     )
@app.route('/feed', methods=['GET','POST'])
@flask_login.login_required
def post_feed():
    return'feed page'

connect=pymysql.connect(
    database="djames_Swipes",
    user="djames",
    password="228118717",
    host="10.100.33.60",
    cursorclass=pymysql.cursors.DictCursor
)