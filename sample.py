from flask import Flask
app = Flask(__name__)

@app.route("/")

def home():
    with open("./virtflask/index.html","rb") as file:
        print("opening file")
        data=file.read()
        return data
    
