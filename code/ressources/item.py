from multiprocessing.dummy import connection
import sqlite3
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
            return item
        
        return {"message":"Item not found  "}

    
        

    def post(self,name):
        if ItemModel.find_by_name(name):
            return {"message": "An item with {} already exists ".format(name)},400
        data=Item.parser.parse_args()
        item={"name":name,"price":data["price"]}
        #Because the insertion can raise an error 
        try:
            ItemModel.insert(item)
        except:
            return {"Message": "An error occured inserting the item."},500 #Internal Server Error
        return item,201
    

    def delete(self,name):
        if ItemModel.find_by_name(name):
            connection=sqlite3.connect("data.db")
            cursor=connection.cursor()
            query="DELETE FROM items WHERE name=? "

            cursor.execute(query,(name,))
            connection.commit()
            connection.close()

        return {"Message": "Item deleted"}
    
    def put(self,name):

        data=Item.parser.parse_args()
        item=ItemModel.find_by_name(name)
        updated_item={"name":name,"price":data["price"]}

        if item is None:
            try:
                ItemModel.insert(updated_item)
            except:
                return {"message":"An error occurred inserting the item"},500
        else:
            try:
                ItemModel.update(updated_item)
            except:
                return {"message":"An error occurred updating the item"},500
        
        return updated_item

 
class ItemList(Resource):
    # def get(self):
    #     return {"items":items}
    def get(self):
        connection=sqlite3.connect("data.db")
        cursor=connection.cursor()
        query="SELECT * from items  "
        result=cursor.execute(query)
        items=[]
        for row in result:
            items.append({"name":row[0],"price":row[1]})

        connection.commit()
        connection.close()

        return {"items":items}