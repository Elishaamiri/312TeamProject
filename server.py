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
        return Success.defaultPageLoad_success("homepage.html","login",request.cookies)
    else:
        # logic for checking the token
        token = request.cookies.get("AuthToken")
        # check the data base to see if this token was issued to a user
        # since all logged out users have an AuthToken value of '' this check ensures that if the Auth token is '' it doesn't try to check to database
        if token == '':
            user = False
        else:
            user = dbm.findUserFromToken(token) 
        if user == False:
            return Success.defaultPageLoad_success("homepage.html","login",request.cookies)
        else:
            return Success.defaultPageLoad_success("basic.html","home",request.cookies)

@app.route("/static/css/<subpath>" ,methods=["GET"])
def send_css(subpath):
    res = make_response(send_from_directory("static/css",subpath))
    res.status_code = "200 OK"
    res.headers['X-Content-Type-Options'] = 'nosniff'
    res.mimetype = mimetypes.guess_type(subpath)[0]
    return res

#@app.route("/static/favicon.ico", methods=["GET"])
#def send_favicon():
#    res = make_response(send_from_directory("static/favicon.ico"))
#    res.status_code = "200 OK"
#    res.headers['X-Content-Type-Options'] = 'nosniff'
#    res.mimetype = "image/x-icon"
#    return res


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
    # checks if both the submitted passwords are the same
    if data['password'] != data['password2']:
        return Errors.register_passwordsDoNotMatch()
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
    token = data["AuthToken"]
    #hashedToken = bcrypt.hashpw(data['AuthToken'].encode('ascii'),util.authSalt)
    dbm.handleLogout(token)
    #db_data.find_one_and_delete({"AuthToken":hashedToken})
    # a = db_data.find({"AuthToken":{'$exists':True}})
    # for i in a:
    #     print(i)
    return Success.logout_success()





@app.route('/submit',methods=["POST"])
def submit():
    data = request.form
    cookies = request.cookies
    
    name = escape(data['recipe_name'])
    description = escape(data['recipe_description'])
    ingredients = escape(data['recipe_ingredients'])
    instructions = escape(data['recipe_instructions'])
    image = request.files['recipe_image'] if 'recipe_image' in request.files else None

    print(f"\n\n\nRecipe name: {name}\nDescription: {description}\ningredients: {ingredients}\ninstructions: {instructions}")
    id = dbm.insertRecipe(name,description,ingredients,instructions,image,cookies)
    return Success.submit_success(name,description,ingredients,instructions,image,id)

@app.route('/recipe',methods=["GET"])
def recipe():
    allRecipes = dbm.allRecipes()
    retList = []
    for x in allRecipes:
        if x.get("deleted") != True:
            cleanx = {key: value for key, value in x.items() if key != '_id'}
            retList.append(cleanx)
    retJSON = json.dumps(retList)
    return Success.getRecipes_success(retJSON)

@app.route('/likeRecipe/<int:recipe_id>',methods=["POST"])
def likeRecipe(recipe_id):
    cookies = request.cookies
    if "AuthToken" not in cookies:
        return Errors.badrequest()
    else:
        # Authtoken exists we can use this to find the username of the individual that liked the recipe
        token = cookies.get("AuthToken")
        name = dbm.findUserFromToken(token)
        if name:
            dbm.updateUserLikes(name,recipe_id)
            return Success.userLike()


        

if __name__ == "__main__":
    app.run("0.0.0.0","8080")


    
    
    
