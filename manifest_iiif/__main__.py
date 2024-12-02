import argparse

from src.manifest import Manifest
from src.config import Config
from src.parsing_csv import Parsing_csv

# A description of the package.
def process_args():
    parser = argparse.ArgumentParser(description="Creates JSON IIIF " 
                                     + "manifests for Nakala datas")
    parser.add_argument("-dataid", "--data_identifier", 
                        help="Nakala data identifier")
    parser.add_argument("-csvfile", "--csv_file", 
                        help="CSV file with data identifier")
    parser.add_argument("-apikey", "--api_key", 
                        help="Nakala user API key")
    parser.add_argument("-annotfile", '--annot_file', 
                        help="Annotation file from Tropy")
    parser.add_argument("-typeannot", '--type_annot', 
                        help="Type of annotation (plain or html)")
    parser.add_argument("-isprod", '--is_prod', help="Production mode")
    parser.add_argument("-csvoutput", "--csv_output", help="CSV output file")
    parser.add_argument("-searchUrl", "--searchBaseUrl", help="Base URL suivi d'un préfix pour le service search")
    parser.add_argument("-method", "--method", help="methode utilisée pour comparer les fichiers lors de la génération d'un manifest avec annotations. Choix entre 'name' et 'sha1'. l'utilisation de 'name' est plus rapide.")

    args = parser.parse_args()
  
    return args

def main():
    args = process_args()
    searchBaseUrl = args.searchBaseUrl if args.searchBaseUrl is not None else "False"
    method = args.method if args.method is not None and (args.method =="name" or args.method =="sha1") else "name"
    nkl_route_path = Config.urlNakala if args.is_prod == "True" else Config.urlTestNakala
    nkl_route_id = Config.urlNakalaId if args.is_prod == "True" else Config.urlTestNakalaId
    if args.csv_file is not None:
        parser = Parsing_csv(args.api_key,args.csv_file, args.type_annot, nkl_route_path, 
                                args.csv_output, searchBaseUrl, nkl_route_id)
        parser.parse_csv()
    elif args.annot_file is None:
        Manifest.create_data_manifest_without_annot_if_data_exists(args.api_key, 
                                                        args.data_identifier, 
                                                        nkl_route_path, 
                                                        args.csv_output, nkl_route_id)
    else:
        Manifest.create_data_manifest_with_annot_if_data_exists(args.api_key, 
                                            args.data_identifier, 
                                            args.annot_file, args.type_annot,
                                            nkl_route_path, args.csv_output, 
                                            searchBaseUrl, method, nkl_route_id)
        

if __name__ == '__main__':
    main()