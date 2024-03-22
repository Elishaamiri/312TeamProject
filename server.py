from flask import Flask, request, render_template, make_response
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

@app.route("/")
def home():
    # we will need to ensure that the authtoken cookie contains a valid auth token tied to an account
    # otherwise anybody can just set an "AuthToken" cookie with any random value and gain access to posting 
    if "AuthToken" not in request.cookies:
        return Success.defaultPageLoad_success("homepage.html")
    else:
        return Success.defaultPageLoad_success("basic.html")
    
@app.route("/static/<path:filepath>")
def getFile(filepath):
    return Success.fileGet_success("/static/"+filepath)

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
    recipeName = data['recipe_name']
    recipeDescription = data['recipe_description']
    recipeIngredients = data['recipe_ingredients']
    recipeInstructions = data['recipe_instructions']
    recipe_image = request.files['recipe_image'] if 'recipe_image' in request.files else None
    return Success.submit_success()



if __name__ == "__main__":
    app.run("0.0.0.0","8080")


    
    
    
