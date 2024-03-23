from flask import make_response

def startingError(errorMsg):
     res = make_response(errorMsg)
     res.headers['"X-Content-Type-Options'] = "nosniff"
     return res

class Errors:
     def login_failed():
          res = startingError("Incorrect Login Info")
          res.status_code = "302 Incorrect Login Info"
          res.location = "/"
          res.mimetype = "text/plain"
          return res
     
     def register_passwordsDoNotMatch():
          res = startingError("Passwords Do Not Match")
          res.status_code = "302 Passwords Do Not Match"
          res.location = "/"
          res.mimetype = "text/plain"
          return res

     def register_userExists():
          res = startingError("User Already Exists")
          res.status_code = "302 User Already Exists"
          res.location = "/"
          res.mimetype = "text/plain"
          return res
     
     def unauthorized_user():
          res = make_response("Unauthorized User")
          res.status_code = "401 Unauthorized User"
          res.mimetype = "text/plain"
          return res

     def nonexistant():
          res = startingError("Requested Item Does Not Exist")
          res.status_code = "404 Does Not Exist"
          res.mimetype = "text/plain"
          return res  

     def form_noData(location):
          res = startingError("Missing Form Data")
          res.status_code = "302 Missing Data"
          res.mimetype = 'text/plain'
          res.location = location
          return res

     def badrequest():
          res = startingError("Bad Request")
          res.status_code = "400 Bad Request"
          res.mimetype = "text/plain"
          return res 