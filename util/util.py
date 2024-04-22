import random
import re
import bcrypt
import hashlib
import base64
from flask import request
GUIDkey = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"


authSalt = b'$2b$12$c4kL2dmcmWvzgLmeQrZrb.'
class Util:
     def generateRandomID(amount):
        id = ""
        for i in range(amount):
                section = random.randrange(0,3)
                if section == 0:
                        id += str(chr(random.randrange(48,57)))
                elif section == 1:
                        id += str(chr(random.randrange(65,90))) 
                else:
                        id += str(chr(random.randrange(97,122)))
        return id
     
     def getInfoThroughAuth(db,request,item):
        AuthToken = request.cookies.get("AuthToken")
        if AuthToken != None:
                        token = bcrypt.hashpw(request.cookies["AuthToken"].encode('ascii'),authSalt)
                        result = db.find_one({"authToken":token})
                        if result == None:
                               return None
                        recievedItem = result[item]
                        return recievedItem
        return None
     
     def compute_accept(websocketKey):
        appendedKey = websocketKey.strip() + GUIDkey
        hashed = hashlib.sha1(appendedKey.encode('ascii'))
        hashed = hashed.digest()
        base64encoding = base64.b64encode(hashed)
        return base64encoding.decode('ascii')
