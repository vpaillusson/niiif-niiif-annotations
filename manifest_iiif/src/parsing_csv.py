import pandas as pd
from src.manifest import Manifest
from src.config import Config

# Parsing CSV file with data identifier and annotation file
class Parsing_csv:
    def __init__(self, apiKey, csv_file, type_annot, nkl_route_path, csv_output, baseUrl, nkl_route_id, method="sha1"):
        """
        Initialize the ParsingCsv object with input parameters.
        :param apiKey: the API key of the Nakala instance
        :param csv_file: the CSV file with data identifier and/or annotation file
        :param type_annot: the type of annotation (plain or html)
        :param nkl_route_path: the route path of the Nakala instance (test or prod)
        :param csv_output: the CSV output file
        """
        self.apiKey = apiKey
        self.csv_file = csv_file
        self.type_annot = type_annot
        self.nkl_route_path = nkl_route_path
        self.csv_output = csv_output
        self.baseUrl = baseUrl
        self.method = method
        self.nkl_route_id = nkl_route_id

    def parse_csv(self):
        """
        Parse input CSV file to determine wich function to call to create the manifest
        :param apiKey: the API key of the Nakala instance
        :param csv_file: the CSV file with data identifier and/or annotation file
        :param type_annot: the type of annotation (plain or html)
        :param nkl_route_path: the route path of the Nakala instance
        (test or prod)
        :param csv_ouput: the CSV output file
        :return: data identifier and annotation file
        """
        
        # Read CSV input file from argument --csv_file
        df = pd.read_csv(self.csv_file, sep=';', keep_default_na=False)
        print(df)

        # Loop on each row of the CSV file
        for index, row in df.iterrows():
            dataIdentifier = row['dcterms:identifier']
            annot_file = row['annotation_file']

            if dataIdentifier != '' :
                if annot_file != '':
                    Manifest.create_data_manifest_with_annot_if_data_exists(
                                                    self.apiKey, 
                                                    dataIdentifier, annot_file, 
                                                    self.type_annot, self.nkl_route_path, 
                                                    self.csv_output, self.baseUrl, self.method, self.nkl_route_id)
                else:
                    Manifest.create_data_manifest_without_annot_if_data_exists(
                                                                    self.apiKey,
                                                                    dataIdentifier,
                                                                    self.nkl_route_path, 
                                                                    self.csv_output, self.nkl_route_id)
            else:
                print("Nakala identifier is needed to create the manifest")
            
        return dataIdentifier, annot_file