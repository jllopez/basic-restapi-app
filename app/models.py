from tortoise.models import Model
from passlib.hash import bcrypt
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator


class User(Model):
    """User DB Model"""
    id = fields.IntField(pk=True)
    username = fields.CharField(50, unique=True)
    password_hash = fields.CharField(128)
    roles = fields.CharField(10, default="user")
    comments: fields.ReverseRelation["Comment"]

    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hash)


class Comment(Model):
    """Comment DB Model"""
    id = fields.IntField(pk=True)
    comment_text = fields.CharField(140)
    likes = fields.IntField()
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="comments")


# Pydantic models for user input and output
user_pyd = pydantic_model_creator(User, name='User')
userin_pyd = pydantic_model_creator(
    User, name='UserIn', exclude_readonly=True)

# Pydantic models for comment input and output
comment_pyd = pydantic_model_creator(Comment, name='Comment')
commentin_pyd = pydantic_model_creator(
    Comment, name='CommentIn', exclude_readonly=True)
