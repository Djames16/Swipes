from flask import Flask, render_template, request, redirect
import pymysql
from pprint import pprint as print
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash


app=Flask(__name__)
auth = HTTPBasicAuth()
@app.route('/')
def index():
    user_name=""
    return render_template(
        "landing.html.jinja",
        user_name=user_name
     )