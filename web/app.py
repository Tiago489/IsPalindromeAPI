from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.isPalindrome
users = db["Users"]

def UserExist(username):
    if users.find({"Username": username}).count() == 0:
        return False
    else:
        return True

def CreateUser(username, password):
    users.insert({
        "Username": username,
        "Password": password,
        "Sentence": ""
    })

def generateResponse(status, message):
    retJson = {
        "status": status,
        "message": message
    }

    return retJson

def validateUser(username, password):
    if not UserExist(username):
        return False

    hashed_pw = users.find({"Username": username})[0]["Password"]

    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False

def palindromeCheck(sentence):
    s = sentence.lower()
    if len(s) < 2:
        return True
    if s[0] != s[-1]:
        return False
    return palindromeCheck(s[1:-1])


class Register(Resource):
    def post(self):

        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]

        if UserExist(username):
            return jsonify(generateResponse(301, "An User already exist with that name"))

        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        CreateUser(username, hashed_pw)

        return jsonify(generateResponse(200, "User sucessfully registed"))

class Detect(Resource):
    def post(self):

        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]
        sentence = postedData["sentence"]

        if validateUser(username, password) == False:
            return jsonify(generateResponse(303, "Invalid Credentials"))

        if palindromeCheck(sentence) == True:
            return jsonify(generateResponse(200, "The sentence " + str(sentence) + " is a palindrome"))
        else:
            return jsonify(generateResponse(304, "The sentence is not a palindrome" ))


api.add_resource(Register, '/register')
api.add_resource(Detect, '/detect')



if __name__=="__main__":
    app.run(host='0.0.0.0')
