import unittest
import pet.models
import pet
from sqlalchemy.exc import OperationalError
import os.path
from mock import MagicMock


class TestPetModels(unittest.TestCase):

    def setUp(self):
        self.isfile = os.path.isfile
        self.engine = pet.engine

    def tearDown(self):
        os.path.isfile = self.isfile
        pet.engine = self.engine

    def test_check_ssl_certificate_with_file(self):
        os.path.isfile = MagicMock(return_value=True)
        pet.engine = MagicMock(return_value=True)
        engine = pet.models.check_ssl_certificate()
        self.assertIsNotNone(engine)

    def test_check_ssl_certificate_with_file_ex(self):
        os.path.isfile = MagicMock(return_value=True)
        pet.engine = MagicMock(side_effect=OperationalError("", {}, None))
        with self.assertRaises(OperationalError) as cm:
            pet.models.check_ssl_certificate()
        self.assertEquals("(NoneType) None", cm.exception.message)

    def test_check_ssl_certificate_no_file(self):
        os.path.isfile = MagicMock(return_value=False)
        pet.engine = MagicMock(return_value=True)
        engine = pet.models.check_ssl_certificate()
        self.assertIsNotNone(engine)

    def test_check_ssl_certificate_no_file_ex(self):
        os.path.isfile = MagicMock(return_value=False)
        pet.engine = MagicMock(side_effect=OperationalError("", {}, None))
        with self.assertRaises(OperationalError) as cm:
            pet.models.check_ssl_certificate()
        self.assertEquals("(NoneType) None", cm.exception.message)
