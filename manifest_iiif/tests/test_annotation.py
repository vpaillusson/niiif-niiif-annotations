import sys
import unittest
import json 

from .config_test import api_key, data_identifier, nkl_route
from src.annotation import Annotation

sys.path.insert(0, '..')

class Test_annotation(unittest.TestCase):
    def setUp(self):
        self.api = api_key
        self.data_identifier = data_identifier
        self.tropy = json.load(open('../annot_img/test.json'))
        self.format_annot = 'plain'
        self.nb_annot = 0
        self.sha1 = 'eb5d2a889c969d34e5fa97b565b3d12e4db8373f'
        self.nkl_route_path = nkl_route
        self.annotation = Annotation.create_annot(self.data_identifier, self.tropy, 
            self.format_annot, self.sha1, self.nb_annot, self.nkl_route_path)

    def test_type_annotation(self):
        self.assertIsInstance(self.annotation, dict)

if __name__ == '__main__':
    unittest.main(verbosity=2)