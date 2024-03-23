import pymongo
from util.errorFunctions import Errors
import util.util as util
import bcrypt
mongo_client = pymongo.MongoClient("mongo")
db = mongo_client["cse312"]

# This file will contain functions that interact directly with the Data Base
# The purpose here is abstraction, no files aside from this one should directly access the data base
# add any and all functions that involve data base operations here


# OPERATIONS FOR USER ACCOUNTS AND RELATED INFORMATION:

# creates a record for user
# arguments: username a plaintext string, password a salted and hashed password
def registerUser(username, password):
    userRecord = db["profiles"]
    userRecord.insert_one({'username':username,'password':password,'AuthToken':''})


# checks if a username already exists
# arguments: username is a string, returns True if username is already tied to an account, False otherwise
def checkUsername(username):
    userRecord = db["profiles"]
    # Check if username exists
    if userRecord.find_one({'username':username}) != None:
        return True
    return False


# handles the login process
# will check if username exists, then if the submitted password matches
# returns the authToken if successful or False if not
def userLogin(username, password):
    userRecord = db["profiles"]
    #Check if username exists and if password is correct
    if userRecord.find_one({'username':username}) == None:
        return False
    try:
        if not bcrypt.checkpw(password.encode('ascii'),userRecord.find_one({'username':username})['password']):
            return False
    except KeyError:
        return False
    #Generate Auth Token Hash it and replace the current auth token or just add a new one
    authToken = util.Util.generateRandomID(64)
    hashedAuthToken = bcrypt.hashpw(authToken.encode('ascii'),util.authSalt)
    userRecord.find_one_and_delete({'username':username,"AuthToken":{"$exists":True}})
    userRecord.insert_one({'username':username,"AuthToken":hashedAuthToken})
    return authToken



# for finding an individuals username using the authentication token
# arguments: token is an unhashed authentication token string
# if the token is valid, returns the name of the user the token was issued to, False otherwise
def findUserFromToken(token):
    # token must be hashed before we check the database
    hashToken = bcrypt.hashpw(token.encode('ascii'),util.authSalt)
    userRecord = db["profiles"]
    try:
        record = list(userRecord.find({"AuthToken":hashToken}))[0]
        username = record["username"]
        return username
    except IndexError:
        return False


# opposite of findUserFromToken
# arguments: username is a plain text username
# returns the value of "AuthToken" tied to the specific username if the username is registered
def findTokenFromUsername(username):
    userRecord = db["profiles"]
    try:
        record = list(userRecord.find({"username":username}))[0]
        token = record["AuthToken"]
        return token
    except IndexError:
        return False












# OPERATIONS FOR RECIPE POSTING

def insertRecipe(recipe, id, cookies):
    recipeBook = db["recipes"]
    token = cookies.get("AuthToken")
    

