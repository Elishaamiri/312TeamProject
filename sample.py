from flask import Flask, request, render_template
from markupsafe import escape
import bcrypt
import util
import mimetypes

app = Flask(__name__)

@app.route("/")
def home():
    authtoken = request.cookies.get('AuthToken')
    file = None
    if authtoken != None:
        return render_template('index.html')
    else:
        return render_template('basic.html')

if __name__ == "__main__":
    app.run()


    
    
    
