from flask import make_response,render_template,send_from_directory
import mimetypes
import json
from util import dataBaseManager as dbm
import bcrypt
import util.util as util
class Success():
     def login_success(authToken):
          res = make_response("User Created")
          res.status_code = "302 User Authorized"
          res.headers['X-Content-Type-Options'] = "nosniff"
          res.location = "/"
          res.set_cookie("AuthToken",authToken,10000,httponly=True)
          res.mimetype = "text/plain"
          
          user = dbm.findUserFromToken(authToken)
          print(f"User: {user} has logged in")

          return res
     
     def defaultPageLoad_success(page,pageType,cookies):
          if pageType == "login":
               res = make_response(render_template(page))
          elif pageType == "home":
               token = cookies.get("AuthToken")
               name = dbm.findUserFromToken(token)
               res = make_response(render_template(page,username=name))
          res.status_code = 200
          res.headers['X-Content-Type-Options'] = "nosniff"
          res.mimetype = "text/html"
          return res
     
     def register_success(username,password):
          res = make_response(json.dumps({'username':username,'password':password}))
          res.status_code = "302 User Created"
          res.location = "/"
          res.headers['X-Content-Type-Options'] = "nosniff"
          res.mimetype = "application/json"
          return res

     def logout_success():
          res = make_response("Logout Successful")
          res.status_code = "302 Logout Successful"
          res.location = "./"
          res.set_cookie("AuthToken",value="Doesnt Matter",max_age=0)
          res.headers['X-Content-Type-Options'] = "nosniff"
          return res

     def submit_success(name,description,ingredients,instructions,image,id):
          name = str(name)
          description = str(description)
          ingredients = str(ingredients)
          instructions = str(instructions)
          res = make_response(json.dumps({'name':name,'description':description,'ingredients':ingredients,'instructions':instructions,'id':id}))
          res.status_code = "302 Created"
          res.mimetype = "application/json"
          res.headers['X-Content-Type-Options'] = "nosniff"
          res.location = "./"
          return res
     
     def username_success(username):
          res = make_response(json.dumps({'username':username}))
          res.status_code = "200 OK"
          res.mimetype = "application/json"
          res.headers['X-Content-Type-Options'] = "nosniff"
          return res

     def getRecipes_success(retJSON):
          res = make_response(retJSON)
          res.status_code = "200 OK"
          res.mimetype = "application/json"
          res.headers['X-Content-Type-Options'] = 'nosniff'
          return res
     
     def userLike():
          res = make_response("liked")
          res.status_code = "302 Liked"
          res.mimetype = "text/plain"
          res.headers['X-Content-Type-Options'] = "nosniff"
          res.location = "./"
          return res
     
     def retLikes():
          res = make_response("likes")
          res.status_code = "200 OK"
          res.mimetype = "text/plain"
          res.headers['X-Content-Type-Options'] = "nosniff"
          #res.location = "./"
          return res