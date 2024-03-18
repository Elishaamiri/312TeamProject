from flask import make_response,render_template
import json

class Success():
     def login_success(authToken):
          res = make_response("User Created")
          res.status_code = 302
          res.headers['"X-Content-Type-Options'] = "nosniff"
          res.location = "/"
          res.set_cookie("AuthToken",authToken,10000,httponly=True)
          res.mimetype = "text/plain"
          return res
     
     def defaultPageLoad_success(page):
          res = make_response(render_template(page))
          res.status_code = 200
          res.headers['"X-Content-Type-Options'] = "nosniff"
          res.mimetype = "text/html"
          return res
     
     def register_success(username,password):
          res = make_response(json.dumps({'username':username,'password':password}))
          res.status_code = 201
          res.headers['"X-Content-Type-Options'] = "nosniff"
          res.mimetype = "application/json"
          return res