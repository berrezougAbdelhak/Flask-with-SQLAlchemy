from importlib.resources import Resource
import sqlite3
from typing_extensions import Required
from flask_restful import Resource,reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument("username",type=str,required=True,help="You have to add the username")
    parser.add_argument("password",type=str,required=True,help="You have to add the password")
    def post(self):
        data=UserRegister.parser.parse_args()
        if not UserModel.find_by_username(data["username"]):
            return {"message": "User exists already"},400

        user=UserModel(data["username"],data["password"])
        user.save_to_db()    
        
        return {"message":"User created successfuly"},201


