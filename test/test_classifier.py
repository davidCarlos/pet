import unittest
import pet.classifier
from pet.classifier import Classifier
import random
import popcon


class FakePackage():
    def __init__(self):
        self.name = ''


class TestPetClassifier(unittest.TestCase):

    def setUp(self):
        pass

    def test_classify_popcon(self):

        package_libdigest_md4_perl = FakePackage()
        package_libdigest_md4_perl.name = 'libdigest-md4-perl'
        package_libsharyanto_utils_perl = FakePackage()
        package_libsharyanto_utils_perl.name = 'libsharyanto-utils-perl'

        packages = [package_libdigest_md4_perl, package_libsharyanto_utils_perl]
        random.shuffle(packages)
        ordered_packages = Classifier.order_packages_by_popcon(packages)

        for i in range(0, len(packages) - 1):
            package1 = popcon.package(ordered_packages[i].name)
            package2 = popcon.package(ordered_packages[i + 1].name)
            self.assertGreaterEqual(package1[ordered_packages[i].name],
                                    package2[ordered_packages[i + 1].name])
