#!/usr/env/python3
""" The file storage engine where the file will be stored """
import sys
import os
import json
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State


class FileStorage:
    """ File Storage class to store the
    to save the obj dict to json string and retrieve
    as Object"""
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """ returns the dictionary objects using json.load """
        return self.__objects

    def new(self, obj):
        """ sets in object with key classname.id """
        clName = obj.__class__.__name__
        k = f"{clName}.{obj.id}"
        self.__objects[k] = obj

    def save(self):
        """ serializes the object into the json file """
        objdict = FileStorage.__objects
        with open(FileStorage.__file_path, "w", encoding="utf-8") as file:
            dict = {key: val.to_dict() for key, val in objdict.items()}
            json.dump(dict, file)

    def reload(self):
        """ deserializes back to python object
        do nothing if the file doesnt exist"""
        if not os.path.isfile(FileStorage.__file_path):
            return
        with open(FileStorage.__file_path, "r", encoding="utf-8") as file:
            pyobj = json.load(file)
            for cl in pyobj.values():
                clName = cl["__class__"]
                del cl["__class__"]
                self.new(eval(clName)(**cl))
