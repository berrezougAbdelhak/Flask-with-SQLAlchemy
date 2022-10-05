from multiprocessing.dummy import connection
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.item import ItemModel
class Item(Resource):
    parser=reqparse.RequestParser() #initialise a new object which we can use to parse the request 
    parser.add_argument("price",type=float,required=True,help="This field cannot be left blank ")
    @jwt_required()
    def get(self,name):
        item=ItemModel.find_by_name(name)

        if item:
            
            return item.json() #because ItemModel returns now a dictionnary 
        
        return {"message":"Item not found  "}

    
        

    def post(self,name):
        if ItemModel.find_by_name(name):
            return {"message": "An item with {} already exists ".format(name)},400
        data=Item.parser.parse_args()
        item=ItemModel(name,data["price"])
        #Because the insertion can raise an error 
        try:
            item.save_to_db()
        except:
            return {"Message": "An error occured inserting the item."},500 #Internal Server Error
        return item.json(),201
    

    def delete(self,name):
        item=ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {"Message": "Item deleted"}
    
    def put(self,name):

        data=Item.parser.parse_args()
        item=ItemModel.find_by_name(name)

        if item is None:
            item=ItemModel(name,data["price"])
        else:
            item.price=data["price"]
        item.save_to_db()    
        
        return item.json()

 
class ItemList(Resource):
    # def get(self):
    #     return {"items":items}
    def get(self):
        

        return {"items":[item.json() for item in ItemModel.query.all()]}