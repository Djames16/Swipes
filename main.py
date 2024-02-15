from flask import Flask, render_template, request, redirect, g
import pymysql
from flask_httpauth import HTTPBasicAuth
import flask_login

app=Flask(__name__)

def connect_db():
    return pymysql.connect(
        host="10.100.33.60",
        user="djames",
        password="228118717",
        database="djames_Swipes",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )

def get_db():
    '''Opens a new database connection per request.'''        
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db    

@app.teardown_appcontext
def close_db(error):
    '''Closes the database connection at the end of request.'''    
    if hasattr(g, 'db'):
        g.db.close() 


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
    
class Posts:
    is_authenticated=True
    is_anonymous=False
    is_active=True
    def __init__(self,id,Description):
        self.Description=Description
        self.id=id
    def get_id(self):
        return str(self.id)

@login_manager.user_loader
def load_user(user_id):
    cursor = get_db().cursor()
    cursor.execute("Select * FROM `User` WHERE `id` =" + str(user_id))
    result=cursor.fetchone()
    cursor.close()
    get_db().commit()
    if result is None:
        return None
    return User(result["id"], result["Username"])

@app.route('/')
def landing_page():
    if flask_login.current_user.is_authenticated:
        return redirect('/feed')
    else: 
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
        cursor = get_db().cursor()
        cursor.execute(f"INSERT INTO `User`(`Username`, `Password`, `Email`, `Description`) VALUES ('{new_username}', '{new_password}','{new_email}', '{new_description}')")
        cursor.close()
        get_db().commit()
    return render_template(
        "Signup.html.jinja"
     )

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        Username=request.form["Username"]
        Password=request.form["Password"]
        cursor = get_db().cursor()
        cursor.execute(f"Select * FROM `User` WHERE `Username` = '{Username}'")
        result=cursor.fetchone()
        cursor.close()
        get_db().commit()
        if Password==result["Password"]:
            User=load_user(result['id'])
            flask_login.login_user(User)
            return redirect('/feed')

    return render_template(
        "Login.html.jinja"
     )

    
@app.route('/feed', methods=['GET','POST'])
@flask_login.login_required
def feed():
    cursor = get_db().cursor()
    cursor.execute(f"Select * FROM `Posts`")
    cursor.close()
    get_db().commit()
    return render_template("Feed.html.jinja")

@app.route('/post',methods=['POST'])
@flask_login.login_required
def create_post():
    description=request.form['description']
    cursor = get_db().cursor()
    cursor.execute("INSERT INTO `posts(`description`, `user_id`)")
    user_id=flask_login.current_user.id