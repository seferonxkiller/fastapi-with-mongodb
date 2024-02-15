# from tortoise import models, fields, Tortoise
# from tortoise.contrib.pydantic import pydantic_model_creator
import binascii
import os

import mongoengine


class User(mongoengine.Document):
    username = mongoengine.StringField(max_length=32)
    password = mongoengine.StringField()


class Token(mongoengine.Document):
    user = mongoengine.ReferenceField(User, unique=True, reverse_delete_rule='CASCADE')
    key = mongoengine.StringField(max_length=40, primary_key=True)
    created_date = mongoengine.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key


class Post(mongoengine.Document):
    user = mongoengine.ReferenceField(User)
    title = mongoengine.StringField(max_length=221)
    body = mongoengine.StringField()
    timestamp = mongoengine.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
# class User(models.Model):
#     id = fields.IntField(pk=True)
#     username = fields.CharField(max_length=23)
#     password = fields.CharField(max_length=16)
#
#     def __str__(self):
#         return self.username
#
#
# class Post(models.Model):
#     id = fields.IntField(pk=True)
#     user = fields.ForeignKeyField("models.User", related_name="user")
#     title = fields.CharField(max_length=221)
#     body = fields.TextField()
#     created_at = fields.DatetimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.title

#
# user_pydantic = pydantic_model_creator(User, name="User")
# user_pydanticIn = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)
#
# post_pydantic = pydantic_model_creator(Post, name="Post")
# post_pydanticIn = pydantic_model_creator(Post, name="PostIn", exclude_readonly=True)
#
