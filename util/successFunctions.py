from flask import make_response,render_template,send_file
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
     
     def defaultPageLoad_success(page):
          res = make_response(render_template(page))
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
     
     def fileGet_success(filepath):
          res = make_response(send_file(filepath),mimetypes.guess_type(filepath)[0])
          res.headers['X-Content-Type-Options'] = 'nosniff'
          return res

     def logout_success():
          res = make_response("Logout Successful")
          res.status_code = "302 Logout Successful"
          res.location = "./"
          res.set_cookie("AuthToken",value="Doesnt Matter",max_age=0)
          res.headers['X-Content-Type-Options'] = "nosniff"
          return res

     def submit_success(name,description,ingredients,instructions,image):
          res = make_response(json.dumps({}))
          res.status_code = "201 Created"
          res.mimetype = "application/json"
          res.headers['X-Content-Type-Options'] = "nosniff"
          return res