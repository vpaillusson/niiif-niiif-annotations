import sys
import unittest
import json

sys.path.insert(0, '..')

class Test_json_Tropy(unittest.TestCase):
    def setUp(self):
        self.json = json.load(open('../annot_img/export_tropy_test.json'))

    #test la valeur de certain champs
    def test_json_equal(self):
        self.assertEqual(self.json['@context']['@version'], 1.1)
        self.assertEqual(self.json['@graph'][0]['title'], 
                        'EFEO_RCA_Aout-Decembre1959_001_01')
        self.assertEqual(self.json['@graph'][0]['photo'][0]['checksum'], 
                         '35a566e76dcf21af828dac7bb4368d7f')

    #test le type de certain champs 
    def test_json_instance(self):
        self.assertIsInstance(self.json['@graph'][0]['title'], str)
        self.assertIsInstance(self.json['@graph'], list)
        self.assertIsInstance(self.json['@graph'][0]['photo'][0]['selection'], 
                              list)
        self.assertIsInstance(self.json['@graph'][0]['photo'][0]['selection'][0], 
                              dict)
        self.assertIsInstance(
            self.json['@graph'][0]['photo'][0]['selection'][0]['@type'],
                               str)
        self.assertIsInstance(self.json['@graph'][0]['photo'][0]['@type'], str)

    #test la présence de certain champs
    def test_json_in(self):
        self.assertIn('@graph', self.json)
        self.assertIn('photo', self.json['@graph'][0])
        self.assertIn('selection', self.json['@graph'][0]['photo'][0])
        self.assertIn('note', self.json['@graph'][0]['photo'][0]['selection'][0])

    #alternative à test_json_instance
    def test_json_true(self):
        self.assertTrue(type(self.json['@graph'][0]['title']) is str)

if __name__ == '__main__':
    unittest.main(verbosity=2)
    