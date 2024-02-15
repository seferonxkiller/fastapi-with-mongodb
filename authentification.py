import hashlib
from models import Token
from fastapi import Request, HTTPException


def hashed_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def verify_password(data_password: str, user_password: str) -> bool:
    return hashlib.sha256(data_password.encode('utf-8')).hexdigest() == user_password


def get_user(req: Request):
    if not req.headers.get('Authorization'):
        raise HTTPException(status_code=401, detail="Not authentificated", headers={"WWW-Authentificate": "token"})
    token = req.headers.get('Authorization').split('token')[1]

    obj = Token(key=token)

    if not token:
        raise HTTPException(status_code=403, detail='Unauthorized')

    if obj is None:
        raise HTTPException(status_code=401, detail='Token is invalid')

    return obj.user

# from passlib.context import CryptContext
# import jwt
# from fastapi.exceptions import HTTPException
# from models import User
# from fastapi import status, Depends
# import main
# from passlib.hash import bcrypt
#
# SECRET = "13088f95d7508110d0e1be376e13d6d47dd6ac5b"
#
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#
#
# def get_password_hash(password):
#     return pwd_context.hash(password)
#
#
# def verify_user(token: str):
#     try:
#         paload = jwt.decode(token, SECRET, algorithms=["HS256"])
#         user = User.objects.get(id=paload["id"])
#     except:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid token",
#             headers={"WWW-Authenticate": "Bearer"}
#         )
#     return user
#
#
# def verify_password(plan_password, hashed_password):
#     return pwd_context.verify(plan_password, hashed_password)
#
#
# def authenticate_user(username: str, password: str):
#     user = User(username=username, password=password)
#     if user and verify_password(password, user.password):
#         return user
#     return False
#
#
# def generate_token(username: str, password: str):
#     user = authenticate_user(username, password)
#
#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password",
#                             headers={"WWW-Authenticate": "Bearer"})
#     data = {
#         id: user.id,
#         username: user.username
#     }
#
#     token = jwt.encode(data, SECRET)
#     return token
