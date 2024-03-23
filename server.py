from flask import Flask, request, render_template, make_response, send_from_directory,url_for
from html import escape
import util.util as util
from util.errorFunctions import Errors
from util.successFunctions import Success
from util import dataBaseManager as dbm
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
    # we will need to ensure that the authtoken cookie contains a valid auth token tied to an account
    # otherwise anybody can just set an "AuthToken" cookie with any random value and gain access to posting 
    if "AuthToken" not in request.cookies:
        return Success.defaultPageLoad_success("homepage.html")
    else:
        # logic for checking the token
        token = request.cookies.get("AuthToken")
        # check the data base to see if this token was issued to a user
        user = dbm.findUserFromToken(token) 
        if user == False:
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
    if dbm.checkUsername(username):
        return Errors.register_userExists()
    
    #Hash password and send to db
    hashedpassword = bcrypt.hashpw(password.encode('ascii'),bcrypt.gensalt())
    dbm.registerUser(username,hashedpassword)
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

    authToken = dbm.userLogin(username,password)
    if authToken == False:
       return Errors.login_failed()
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





@app.route('/submit',methods=["POST"])
def submit():
    data = request.form
    name = data['recipe_name']
    description = data['recipe_description']
    ingredients = data['recipe_ingredients']
    instructions = data['recipe_instructions']
    image = request.files['recipe_image'] if 'recipe_image' in request.files else None
    return Success.submit_success(name,description,ingredients,instructions,image)



if __name__ == "__main__":
    app.run("0.0.0.0","8080")


    
    
    
