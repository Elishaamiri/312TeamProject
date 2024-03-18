from flask import make_response

def startingError(errorMsg):
     res = make_response(errorMsg)
     res.headers['"X-Content-Type-Options'] = "nosniff"
     return res

class Errors:
     def login_failed():
          res = startingError("Incorrect Login Info")
          res.status_code = 302
          res.location = "/"
          res.mimetype = "text/plain"
          return res

     def unauthorized_user():
          res = make_response("Unauthorized User")
          res.status_code = 401
          res.mimetype = "text/plain"
          return res

     def nonexistant():
          res = startingError("Requested Item Does Not Exist")
          res.status_code = 404
          res.mimetype = "text/plain"
          return res  

     def badrequest():
          res = startingError("Bad Request")
          res.status_code = 400
          res.mimetype = "text/plain"
          return res 