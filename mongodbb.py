from fastapi import FastAPI
from pymongo import MongoClient
from tortoise import Tortoise, fields, models
from models import user_pydantic

app = FastAPI()

# Configure Tortoise-ORM for MongoDB using Motor driver
# TORTOISE_ORM = {
#     "connections": {
#         "default": "mongodb://localhost:27017/mydatabase"
#     },
#     "apps": {
#         "models": {
#             "models": ["main"],
#             "default_connection": "default",
#         }
#     }
# }
client = MongoClient("mongodb://localhost:27017/fastapi")

db = client.fastapi
collection_name = db["todos_app"]


# Tortoise model
class User(models.Model):
    name = fields.CharField(max_length=255)


# Initialize Tortoise
Tortoise.init_models(["main"], "models")
Tortoise.generate_schemas()


# Route to get all users from MongoDB
@app.get("/users")
async def get_users():
    user = await user_pydantic.from_queryset(User.all())
    # users = await User.all()
    # return {"users": [{"name": user.username} for user in users]}
    return {"status": 200, "data": user}
