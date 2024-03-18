from flask import Flask, request, render_template, make_response
from html import escape
import util.util as util
from util.errorFunctions import Errors
from util.successFunctions import Success
import bcrypt
import mimetypes
import json
import pymongo

app = Flask(__name__)
mongo_client = pymongo.MongoClient('mongo')
db = mongo_client["cse312"]
db_data = db['data']


@app.route("/")
def home():
    if "AuthToken" not in request.cookies:
        return Success.defaultPageLoad_success("index.html")
    else:
        return Success.defaultPageLoad_success("basic.html")
    
@app.route("/static/<path:filepath>")
def getFile(filepath):
    return Success.fileGet_success("/static/"+filepath)

@app.route('/register',methods=['POST'])
def register():
    data = request.get_json()

    #Checks if there is missing data
    if 'username' not in data or 'password' not in data:
        return Errors.badrequest()
    
    #Escapes characters
    username = escape(data['username'])
    password = escape(data['password'])

    #Check if username exists
    if db_data.find_one({'username',username}) != None:
        return Errors.badrequest()
    
    #Hash password and send to db
    hashedpassword = bcrypt.hashpw(password,bcrypt.gensalt())
    db_data.insert_one({'username':username,'password':hashedpassword})

    #Return Success Message
    return Success.register_success(data['username'],data['password'])

@app.route('/login',methods=['POST'])
def login():
    data = request.get_json()
    
    #Checks if there is missing data
    if 'username' not in data or 'password' not in data:
        return Errors.badrequest()

    #Escapes characters
    username = escape(data['username'])
    password = escape(data['password'])

    #Check if username exists and if password is correct
    if db_data.find_one({'username',username}) == None:
        return Errors.badrequest()
    if not bcrypt.checkpw(password,db_data.find_one({'username':username})['password']):
        return Errors.login_failed()

    #Generate Auth Token Hash it and replace the current auth token or just add a new one
    authToken = util.Util.generateRandomID(64)
    hashedAuthToken = bcrypt.hashpw(authToken,util.authSalt)
    db_data.find_one_and_delete({'username':username,"AuthToken":{"$exists":True}})
    db_data.insert_one({'username':username,"AuthToken":hashedAuthToken})

    #Return Success Message
    return Success.login_success(authToken)

if __name__ == "__main__":
    app.run("0.0.0.0","8080")


    
    
    
