import sys
import unittest

from .config_test import api_key, data_identifier, nkl_route
from src.metadata import Metadata
from src.connection_api import Connection_Nakala

sys.path.insert(0, '..')

class Test_json_Metadata(unittest.TestCase):
    def setUp(self):
        self.api = api_key
        self.data_identifier = data_identifier
        self.nkl_route_path = nkl_route
        
        self.response = Connection_Nakala.get_data_metadata(self.api, 
                                                            self.data_identifier,
                                                            self.nkl_route_path)

        self.metadatas = self.response.json()['metas']
        self.metadata_example = [{'label': 'Title', 'value': 'EFEO RCA'},
            {'label': 'Creator', 'value': 'Anonyme'},
            {'label': 'Created', 'value': None},
            {'label': 'License', 'value': 'CC-BY-4.0'},
            {'label': 'Type', 'value': 'http://purl.org/coar/resource_type/c_c513'}]

    #Test la connection à l'API Nakala
    def test_connection_Nakala(self):
        self.assertEqual(self.response.status_code, 200)

    #Test le type d'instance du json de réponse
    def test_metadata_Nakala(self):
        self.assertIsInstance(self.metadatas, list)

    #Test la valeur de certain champs
    def test_metadata_fields(self):
        self.assertEqual(self.metadatas[0]['propertyUri'],
                        'http://nakala.fr/terms#title')
        self.assertEqual(self.metadatas[1]['propertyUri'], 
                        'http://nakala.fr/terms#creator')

    #Test parsing json de réponse
    def test_metadata_parse(self):
        self.assertIsInstance(Metadata.create_metadata(self.metadatas), list)

        #Méthode de test pour vérifier que le json de réponse n'est pas vide
        self.assertIsNotNone(Metadata.create_metadata(self.metadatas))

        #Méthode de test de la structure du json de réponse
        self.assertListEqual(Metadata.create_metadata(self.metadatas), 
                            self.metadata_example)

if __name__ == '__main__':
    unittest.main(verbosity=2)
    