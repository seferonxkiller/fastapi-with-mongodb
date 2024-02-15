from typing import Dict, Any, List

from fastapi import FastAPI, HTTPException
# from mongoengine import connect, Document, StringField
import mongoengine
from pydantic import BaseModel

# Connect to MongoDB
db = mongoengine.connect(db='mydatabase', host='mongodb://localhost:27017')


# Define a MongoDB document model
class Item(mongoengine.Document):
    name = mongoengine.StringField(max_length=255)


# class ItemBaseModel(BaseModel):
#     students: List[Item]


app = FastAPI()


# item_collection = db.get_collection("item")


@app.post("/items/")
async def create_item(name: str):
    # Create a new item in MongoDB
    item = Item(name=name)
    item.save()

    return {"message": "Item created successfully", "item_id": str(item.id)}


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    try:
        item = Item.objects.get(id=item_id)
        return {"item_id": str(item.id), "name": item.name}
    except Item.DoesNotExist:
        raise HTTPException(status_code=404, detail="Item not found")


import json


@app.get("/items")
async def get_all_items():
    items = Item.objects()
    lst = []
    for item in items:
        lst.append({"item_id": str(item.id), "name": item.name})

    return lst




@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    item = Item.objects.get(id=str(item_id))
    item.delete()
    return {'status': 204}