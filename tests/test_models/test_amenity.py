#!/usr/bin/python3
""" unittest for amenity class """
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.amenity import Amenity
import datetime
import json
import os
from time import sleep
import models
import unittest


class TestAmenity_save(unittest.TestCase):
    """ test save method for Amenity class """
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

    def test_save_for_amenity_object(self):
        """ test_save_for_amenity_object """
        amenity = Amenity()
        amenity.save()
        Amkey = "Amenity." + amenity.id
        with open("file.json", "r") as file:
            self.assertIn(Amkey, file.read())

    def test_save_and_pass_argument(self):
        """ test_save_and_pass_argument """
        amenity = Amenity()
        with self.assertRaises(TypeError):
            amenity.save(None)

    def test_save_on_two_calls(self):
        """ test save for two different calls """
        amenity = Amenity()
        sleep(0.1)
        updated_at_1 = amenity.updated_at
        amenity.save()
        updated_at_2 = amenity.updated_at
        self.assertLess(updated_at_1, updated_at_2)
        sleep(0.1)
        amenity.save()
        self.assertLess(updated_at_2, amenity.updated_at)


class TestAmenity_to_dict(unittest.TestCase):
    """class to test to_dict method for Amenity class """
    def test_to_dict_keys_if_same(self):
        """  """

    def test_to_dict_type(self):
        """ test_to_dict_type """
        amenity = Amenity()
        self.assertTrue(dict, type(amenity.to_dict()))

    def test_to_dict_with_None_arg(self):
        """ test_to_dict_with_None_arg """
        amenity = Amenity()
        with self.assertRaises(TypeError):
            amenity.to_dict(None)

    def test_if_to_dict_kv_is_same_with__dict__(self):
        """ check if  test passes the  missing __class__ in __dict__"""
        amenity = Amenity()
        self.assertNotEqual(amenity.to_dict(), amenity.__dict__)


if __name__ == "__main__":
    unittest.main()
