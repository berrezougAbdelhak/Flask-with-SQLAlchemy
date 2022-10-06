from flask import Flask
from  flask_restful import  Api
from flask_jwt import JWT,jwt_required
from security import authenticate,identity
from ressources.user import UserRegister
from ressources.item import Item,ItemList 
from ressources.store import Store,StoreList

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False # turns off the flask sqlalchemy modification tracker  
app.secret_key="jose"
api=Api(app)

@app.before_first_request
def create_tables():
    db.create_all()


jwt=JWT(app,authenticate,identity)


items=[] 

         
api.add_resource(Item,"/item/<string:name>") 

api.add_resource(ItemList,"/items")

api.add_resource(UserRegister,"/register")

api.add_resource(Store,"/store/<string:name>")

api.add_resource(StoreList,"/stores")

if __name__=="__main__":
    from db import db 
    db.init_app(app)
    app.run(port=5000,debug=True)