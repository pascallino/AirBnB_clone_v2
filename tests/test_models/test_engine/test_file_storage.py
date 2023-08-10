#!/usr/bin/python3
"""unittest Module for FileStorage class"""

from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.engine.file_storage import FileStorage
import datetime
import json
import os
import models
import unittest


class TestFileStorage_save(unittest.TestCase):
    """ test save method in Filestorage class """
    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "pascal")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("pascal", "file.json")
        except IOError:
            pass

    def clearStorage(self):
        """ clear the file contents """
        FileStorage._FileStorage__objects = {}
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("pascal", "file.json")
        except IOError:
            pass

    def test_save_bypassing_None_parameter(self):
        """ test_save_bypassing_None_parameter """
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def test_save_method(self):
        """ test save function in filestorage class"""
        bmodel = BaseModel()
        user = User()
        state = State()
        place = Place()
        city = City()
        amenity = Amenity()
        review = Review()
        models.storage.new(bmodel)
        models.storage.new(user)
        models.storage.new(state)
        models.storage.new(place)
        models.storage.new(city)
        models.storage.new(amenity)
        models.storage.new(review)
        models.storage.save()
        with open("file.json", 'r') as file:
            getllobjs = file.read()
        self.assertIn("BaseModel." + bmodel.id, getllobjs)
        self.assertIn("User." + user.id, getllobjs)
        self.assertIn("State." + state.id, getllobjs)
        self.assertIn("Place." + place.id, getllobjs)
        self.assertIn("City." + city.id, getllobjs)
        self.assertIn("Amenity." + amenity.id, getllobjs)
        self.assertIn("Review." + review.id, getllobjs)


class TestFileStorage_reload(unittest.TestCase):
    """ test reload method in Filestorage class """
    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "pascal")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("pascal", "file.json")
        except IOError:
            pass

    def clearStorage(self):
        """ clear the file contents """
        FileStorage._FileStorage__objects = {}
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("pascal", "file.json")
        except IOError:
            pass

    def test_reload(self):
        """ test_reload function"""
        bmodel = BaseModel()
        user = User()
        state = State()
        place = Place()
        city = City()
        amenity = Amenity()
        review = Review()
        models.storage.new(bmodel)
        models.storage.new(user)
        models.storage.new(state)
        models.storage.new(place)
        models.storage.new(city)
        models.storage.new(amenity)
        models.storage.new(review)
        models.storage.save()
        models.storage.reload()
        getllobjs = FileStorage._FileStorage__objects
        self.assertIn("BaseModel." + bmodel.id, getllobjs)
        self.assertIn("User." + user.id, getllobjs)
        self.assertIn("State." + state.id, getllobjs)
        self.assertIn("Place." + place.id, getllobjs)
        self.assertIn("City." + city.id, getllobjs)
        self.assertIn("Amenity." + amenity.id, getllobjs)
        self.assertIn("Review." + review.id, getllobjs)

    def test_reload_bypassing_None_parameter(self):
        """ test_reload_bypassing_None_parameter """
        with self.assertRaises(TypeError):
            models.storage.reload(None)


class TestFileStorage_all(unittest.TestCase):
    """ Test all method for file storage"""
    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "pascal")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("pascal", "file.json")
        except IOError:
            pass

    def clearStorage(self):
        """ clear the file contents """
        FileStorage._FileStorage__objects = {}
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("pascal", "file.json")
        except IOError:
            pass

    def test_all(self):
        """ test all type """
        self.assertEqual(dict, type(models.storage.all()))

    def test_all_with_none_parameter(self):
        """ test all with none arg"""
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def test_all_method(self):
        """ test_all_method """
        bmodel = BaseModel()
        user = User()
        state = State()
        place = Place()
        city = City()
        amenity = Amenity()
        review = Review()
        models.storage.new(bmodel)
        models.storage.new(user)
        models.storage.new(state)
        models.storage.new(place)
        models.storage.new(city)
        models.storage.new(amenity)
        models.storage.new(review)
        models.storage.save()
        getllobjs = models.storage.all().keys()
        self.assertIn("BaseModel." + bmodel.id, getllobjs)
        self.assertIn("User." + user.id, getllobjs)
        self.assertIn("State." + state.id, getllobjs)
        self.assertIn("Place." + place.id, getllobjs)
        self.assertIn("City." + city.id, getllobjs)
        self.assertIn("Amenity." + amenity.id, getllobjs)
        self.assertIn("Review." + review.id, getllobjs)


if __name__ == "__main__":
    unittest.main()
