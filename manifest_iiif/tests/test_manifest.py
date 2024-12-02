import sys
import unittest 
import json

from .config_test import api_key, data_identifier, nkl_route
from src.connection_api import Connection_Nakala
from src.manifest import Manifest

sys.path.insert(0, '..')

#test du manifeste
class Test_manifest(unittest.TestCase):
    def setUp(self):
        self.json_manifest = json.load(open('../annot_img/manifest_for_unit_test.json'))
        self.api = api_key
        self.data_identifier = data_identifier
        self.nkl_route_path = nkl_route
        
        self.format_annot = 'plain'
        self.json_annot_tropy = '../annot_img/export_tropy_test.json'
        self.csv_output = 'output_test.csv'

        '''
        self.manifest_annot = \
            Manifest.create_data_manifest_with_annot_if_data_exists(self.api, 
                                                            self.data_identifier, 
                                                            self.json_annot_tropy, 
                                                            self.format_annot,
                                                            self.nkl_route_path,
                                                            self.csv_output)
        self.manifest = \
            Manifest.create_data_manifest_without_annot_if_data_exists(
                                                            self.api, 
                                                            self.data_identifier,
                                                            self.nkl_route_path,
                                                            self.csv_output)
        '''

    def test_manifest_structure(self):
        self.assertIn('metadata', self.json_manifest)
        self.assertIn('rendering', self.json_manifest)
        self.assertIn('items', self.json_manifest)
        self.assertIn('annotations', self.json_manifest['items'][0])
        self.assertIn('thumbnail', self.json_manifest['items'][0])


    def test_manifest__type(self):
        self.assertIsInstance(self.json_manifest['metadata'], list)
        self.assertIsInstance(self.json_manifest['rendering'], list)
        self.assertIsInstance(self.json_manifest['items'], list)
        self.assertIsInstance(self.json_manifest['items'][0]['annotations'], list)
        self.assertIsInstance(self.json_manifest['items'][0]['thumbnail'], list)

    '''
    def test_manifest_creation(self):
        self.assertIsNotNone(self.json_manifest)
    '''
    
if __name__ == '__main__':
    unittest.main(verbosity=20)