import unittest
import pet.ci_debian_packages as ci
import re


class TestPetCi(unittest.TestCase):


    def test_if_file_is_registered(self):
        ci.get_packages_from_url()

        try:
            file = open("packages.json", "r")
        except IOError:
            file = None

        self.assertNotEqual(None, file)

    def test_if_data_is_a_list(self):
        data = ci.get_ci_debian_json()

        self.assertEquals(isinstance(data, list), True)

    def test_if_element_is_dict(self):
        data = ci.get_ci_debian_json()
        package = data[0]

        self.assertEquals(isinstance(package, dict), True)
