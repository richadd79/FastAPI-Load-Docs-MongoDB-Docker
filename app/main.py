from fastapi import FastAPI

# Both used for BaseModel
from pydantic import BaseModel

#Mongo
from pymongo import MongoClient
import json

# You need this to be able to turn classes into JSONs and return
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


# Create class (schema) for the JSON
# Date get's ingested as string and then before writing validated
class PurchaseItem(BaseModel):
    event_time: str
    order_id: int
    category_id: int
    brand: str
    price: float
    user_id: int
    category: str
    product: str

app = FastAPI()

# Base URL
@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI with MongoDB"}


myclient = MongoClient("mongodb://root:example@mongo:27017/admin?authSource=admin")
mydb = myclient["test"] # select the database
mycol = mydb["testcol"] # select the collection

# Add a new purchase
@app.post("/purchaseitem")
async def post_purchase_item(item: PurchaseItem): #body awaits a json with purchase item information
    print("Message received")

    # Parse item back to json
    json_of_item = jsonable_encoder(item)

    x = mycol.insert_one(json_of_item)

    print(x.inserted_id)

    json_compatible_item_data = jsonable_encoder(item)
    return JSONResponse(content=json_compatible_item_data)




