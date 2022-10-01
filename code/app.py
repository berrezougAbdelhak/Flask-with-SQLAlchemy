from flask import Flask
from  flask_restful import  Api
from flask_jwt import JWT,jwt_required
from security import authenticate,identity
from ressources.user import UserRegister
from ressources.item import Item,ItemList 


app=Flask(__name__)
app.secret_key="jose"
api=Api(app)

jwt=JWT(app,authenticate,identity)


items=[] 

         
api.add_resource(Item,"/item/<string:name>") 

api.add_resource(ItemList,"/items")

api.add_resource(UserRegister,"/register")

if __name__=="__main__":
    app.run(port=5000,debug=True)