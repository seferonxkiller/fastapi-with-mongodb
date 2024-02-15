from fastapi import FastAPI, HTTPException, status, Depends
import mongoengine
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import models
import authentification

db = mongoengine.connect(db='fastapi', host='localhost', port=27017)
app = FastAPI(title="Mongodb crud")


# oauth2_bearer = OAuth2PasswordBearer(tokenUrl='token')


class UserModel(BaseModel):
    username: str
    password: str


class PostModel(BaseModel):
    user: str
    title: str
    body: str


class RegisterModel(BaseModel):
    username: str
    password: str
    password2: str


class UserBase(BaseModel):
    username: str


@app.post("/user")
async def post_user(data: RegisterModel):
    if data.password != data.password2:
        return {"message": "Password is not correct"}
    data.password = authentification.hashed_password(data.password)
    del data.password2
    user = models.User(**data.dict(exclude_unset=True))
    print(user.password)
    user.save()
    print(user.__dict__)
    data = data.__dict__
    # data = UserModel(**user.__dict__).dict()
    token = models.Token(user=user)
    token.save()
    data["token"] = token.key
    return data


@app.post("/login")
async def login_user(data: UserModel):
    user = models.User.objects(username=data.username).first()
    print(user.password)
    # print(user.__dict__)
    # print(user.id)
    # print(user)
    if not user:
        return {"message": "Invalid username"}
    if not authentification.verify_password(data.password, user.password):
        return {"message": "Invalid password"}
    token = models.Token.objects.get(user=user.id)
    return {'token': token.key}


# crud for user
# dependencies=[Depends(authentification.get_user)]
@app.get("/users", dependencies=[Depends(authentification.get_user)])
async def get_users():
    users = models.User.objects()
    lt = []
    for a in users:
        lt.append({"user_id": str(a.id), "username": a.username})
    return lt


# @app.post("/users")
# async def create_user(user: UserModel):
#     obj = models.User(username=user.username, password=user.password)
#     obj.save()
#     return {"id": str(obj.id), "username": obj.username}


@app.get("/users/{user_id}")
async def get_user(user_id: str):
    try:
        obj = models.User.objects.get(id=user_id)
        return {'user_id': str(obj.id), 'username': obj.username}
    except models.User.DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")


@app.delete("/users/{user_id}")
async def delete_user(user_id: str):
    obj = models.User.objects.get(id=user_id)
    obj.delete()
    return {"success": True, "status": 204}


# crud for post


@app.get("/posts")
async def get_posts():
    posts = models.Post.objects()

    list = []
    for post in posts:
        list.append({'id': str(post.id), 'title': post.title})

    return list


@app.post("/post")
async def create_post(post: PostModel):
    user = models.User.objects.get(username=post.user)
    print(post.user)
    print(user.username)
    try:
        obj = models.Post(title=post.title, body=post.body, user=post.user)
        obj.save()
        return {"id": str(obj.id), "title": obj.title, "body": obj.body}
    except models.User.DoesntExists:
        return {"success": False, "message": "User not found"}


@app.get("posts/{post_id}")
async def get_post(post_id: str):
    try:
        post = models.Post.objects.get(id=post_id)
        return {"title": post.title, "body": post}

    except models.Post.DoesNotExist:
        raise HTTPException(status_code=404, detail="Post not found")


@app.delete("/posts/{post_id}")
async def delete_post(post_id: str):
    obj = models.Post.objects.get(id=post_id)
    obj.delete()
    return {'status': 204}

# register_tortoise(
#     app,
#     config=TORTOISE_ORM,
#     generate_schemas=True,
#     add_exception_handlers=True
# )

#
# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
#
# @app.get("/users")
# async def get_users():
#     user = await user_pydantic.from_queryset(User.all())
#     print(await user_pydantic.from_queryset(User.all()))
#     # users = await User.all()
#     # return {"users": [{"name": user.username} for user in users]}
#     return {"status": 200, "data": user}
#
#
# @app.get("/posts")
# async def get_posts():
#     return await Post.all()
#
#
# @app.post("/posts")
# async def create_post(post: post_pydanticIn):
#     post = post.dict(exclude_unset=True)
#
#     post_obj = await Post.create(**post)
#     post_obj = await post_pydantic.from_tortoise_orm(post_obj)
#
#     return {"status": 201, "post": post_obj}
#
#
# @app.post("/user")
# async def creat_user(user: user_pydanticIn):
#     user = user.dict(exclude_unset=True)
#
#     user_obj = await User.create(**user)
#     user_obj = await user_pydantic.from_tortoise_orm(user_obj)
#
#     return {"status": 201, "user": user_obj}
