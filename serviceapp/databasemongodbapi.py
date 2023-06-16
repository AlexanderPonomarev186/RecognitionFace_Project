from mongoengine import *
import uuid

class User(Document):
    # id = UUIDField(required=True)
    name = StringField(required=True)
    face_vector = ListField(required=True)


def createuser(name: str, face_vector: list):
    User(name=name, face_vector=face_vector).save()