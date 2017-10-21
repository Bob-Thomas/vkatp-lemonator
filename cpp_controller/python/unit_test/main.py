import unittest
import os
from lemonator_test import LemonatorInterfaceTest
from plant_test import PlantTest
from vessel_test import VesselTest
from controller_test import ControllerTest
# def load_tests(loader, tests, pattern):
#     suite = unittest.TestSuite()
#     for all_test_suite in unittest.defaultTestLoader.discover('./', pattern='*_test.py'):
#         for test_suite in all_test_suite:
#             suite.addTests(test_suite)
#     return suite

test_cases = (LemonatorInterfaceTest, VesselTest, PlantTest, ControllerTest)


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    for test_class in test_cases:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    return suite


if __name__ == '__main__':
    unittest.main(verbosity=2)
