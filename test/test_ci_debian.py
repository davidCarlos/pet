import unittest
import pet.ci as ci


class TestPetCi(unittest.TestCase):

    def test_if_file_is_registered(self):
        url = "https://ci.debian.net/data/status/unstable/amd64/packages.json"
        ci.get_packages_from_url(url)

        try:
            file = open("pet/.debian_ci/packages.json", "r")
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

    def test_file_not_found(self):
        response = ci.found_on_json("without_this_package")
        self.assertEquals(response, False)
