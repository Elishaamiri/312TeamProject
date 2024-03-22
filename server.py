from flask import Flask, request, render_template, make_response, send_from_directory,url_for
from html import escape
import util.util as util
from util.errorFunctions import Errors
from util.successFunctions import Success
import bcrypt
import mimetypes
import json
import pymongo

app = Flask(__name__)
mongo_client = pymongo.MongoClient("mongo")
db = mongo_client["cse312"]
db_data = db['data']


@app.route("/", methods=["GET"])
def home():
    if "AuthToken" not in request.cookies:
        return Success.defaultPageLoad_success("homepage.html")
    else:
        return Success.defaultPageLoad_success("basic.html")

@app.route("/static/css/<subpath>" ,methods=["GET"])
def send_css(subpath):
    res = make_response(send_from_directory("static/css",subpath))
    res.status_code = "200 OK"
    res.headers['X-Content-Type-Options'] = 'nosniff'
    res.mimetype = mimetypes.guess_type(subpath)[0]
    return res

@app.route("/static/images/<subpath>" ,methods=["GET"])
def send_images(subpath):
    res = make_response(send_from_directory("static/images",subpath))
    res.status_code = "200 OK"
    res.headers['X-Content-Type-Options'] = 'nosniff'
    res.mimetype = mimetypes.guess_type(subpath)[0]
    return res

@app.route("/static/js/<subpath>" ,methods=["GET"])
def send_js(subpath):
    res = make_response(send_from_directory("static/js",subpath))
    res.status_code = "200 OK"
    res.headers['X-Content-Type-Options'] = 'nosniff'
    res.mimetype = mimetypes.guess_type(subpath)[0]
    return res

@app.route('/register',methods=['POST'])
def register():
    data = request.form
    #Checks if there is missing data
    if 'username' not in data or 'password' not in data:
        return Errors.badrequest()
    #Escapes characters
    username = escape(data['username'])
    password = escape(data['password'])
    #Check if username exists
    if db_data.find_one({'username':username}) != None:
        return Errors.register_userExists()
    #Hash password and send to db
    hashedpassword = bcrypt.hashpw(password.encode('ascii'),bcrypt.gensalt())
    db_data.insert_one({'username':username,'password':hashedpassword})
    #Return Success Message
    return Success.register_success(data['username'],data['password'])

@app.route('/login',methods=['POST'])
def login():
    data = request.form
    #Checks if there is missing data
    if 'username' not in data or 'password' not in data:
        return Errors.badrequest()

    #Escapes characters
    username = escape(data['username'])
    password = escape(data['password'])

    #Check if username exists and if password is correct
    if db_data.find_one({'username':username}) == None:
        return Errors.login_failed()
    if not bcrypt.checkpw(password.encode('ascii'),db_data.find_one({'username':username})['password']):
        return Errors.login_failed()

    #Generate Auth Token Hash it and replace the current auth token or just add a new one
    authToken = util.Util.generateRandomID(64)
    hashedAuthToken = bcrypt.hashpw(authToken.encode('ascii'),util.authSalt)
    db_data.find_one_and_delete({'username':username,"AuthToken":{"$exists":True}})
    db_data.insert_one({'username':username,"AuthToken":hashedAuthToken})

    #Return Success Message
    return Success.login_success(authToken)

@app.route('/logout',methods=["POST"])
def logout():
    data = request.cookies
    hashedToken = bcrypt.hashpw(data['AuthToken'].encode('ascii'),util.authSalt)
    db_data.find_one_and_delete({"AuthToken":hashedToken})
    # a = db_data.find({"AuthToken":{'$exists':True}})
    # for i in a:
    #     print(i)
    return Success.logout_success()


if __name__ == "__main__":
    app.run("0.0.0.0","8080")


    
    
    
