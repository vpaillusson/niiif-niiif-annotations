from src.hash import hash_pictures
from src.config import Config
import requests
import json

class Annotation:
    @staticmethod
    def create_annot(annot_file_open, sha1, idFile, number_annot, formatAnnot, nkl_route_path, fileName, method):
        """
        Returns a list of annotation objects for the image.
        :param annot_file_open: JSON file of Tropy
        :param sha1: SHA1 of the image
        :param idFile: ID of the file
        :param number_annot: Number of annotation
        :param formatAnnot: Format of annotation
        :param nkl_route_path: The route path of the Nakala instance (test or prod)
        :param fileName: The name of the file in Nakala
        :param method: the method used to compare files in local storage and in nakala (either name or sha1 which is much more time consuming)
        :return: List of annotation JSON objects
        """
        annot = []
        #print(f"length annot file: {len(annot_file_open['@graph'])}")
        #print(type(annot_file_open))
        # Parsing JSON Tropy for annotation
        for i in annot_file_open["@graph"]:
        #for i in range(1, len(annot_file_open['@graph']), 1):
        #for cle, valeur in annot_file_open.items():
            #print(f"graph = {i}")
            for p in i["photo"]:
                #p = annot_file_open["@graph"][i].get("photo")[0]
                #print(f"photo = {p}")
                filename_path = p.get("path")
                tropy_filename = p.get("filename")
                #filename_path = p[0]["path"]
                #print("traitement du fichier image "+filename_path)
                if filename_path:
                    tropy_file = tropy_filename if method == "name" else  hash_pictures(filename_path)
                    nakala_file = fileName if method == "name" else sha1
                    #hash_file = hash_pictures(filename_path)
                    if tropy_file == nakala_file:
                        #print("fichier "+ filename_path +" same as in Nakala ressource" + hash_file)
                        for x in p.get("selection", []):
                            loc = f"/Canvas#xywh={x['x']},{x['y']},{x['width']},{x['height']}"
                            url_annot = nkl_route_path + Config.nakala_url_iiif
                            target = f"{url_annot}{idFile}{loc}"
                            number_annot += 1
                            count_annot = f"/annot_{number_annot}"
                            annot_count_arg = Config.annot_url_arg + count_annot

                            for y in x.get('note', []):
                                annotation_value = str(y["html"]["@value"])
                                id_annot = f"{url_annot}{idFile}{annot_count_arg}"

                                annot.append({
                                    "id": id_annot,
                                    "type": "Annotation",
                                    "motivation": "commenting",
                                    "body": [
                                        {
                                            "type": "Textualbody",
                                            "value": annotation_value,
                                            "language": "fr",
                                            "format": f"text/{formatAnnot}"
                                        }
                                    ],
                                    "target": target
                                })
                        return annot


    @staticmethod
    def create_annot_fast(file,idFile,number_annot, formatAnnot, nkl_route_path):
        # méthode non encore terminée pour générer un manifest directement à partir de données Tropy 
        """
        Returns a list of annotation objects for the image.
        :param annot_file_open: JSON file of Tropy
        :param sha1: SHA1 of the image
        :param idFile: ID of the file
        :param number_annot: Number of annotation
        :param formatAnnot: Format of annotation
        :param nkl_route_path: The route path of the Nakala instance (test or prod)
        :param fileName: The name of the file in Nakala
        :return: List of annotation JSON objects
        """
        annot = []
       
        for x in file.get("selection", []):
            loc = f"/Canvas#xywh={x['x']},{x['y']},{x['width']},{x['height']}"
            url_annot = nkl_route_path + Config.nakala_url_iiif
            target = f"{url_annot}{idFile}{loc}"
            number_annot += 1
            count_annot = f"/annot_{number_annot}"
            annot_count_arg = Config.annot_url_arg + count_annot

            for y in x.get('note', []):
                annotation_value = str(y["html"]["@value"])
                id_annot = f"{url_annot}{idFile}{annot_count_arg}"

                annot.append({
                    "id": id_annot,
                    "type": "Annotation",
                    "motivation": "commenting",
                    "body": [
                        {
                            "type": "Textualbody",
                            "value": annotation_value,
                            "language": "fr",
                            "format": f"text/{formatAnnot}"
                        }
                    ],
                    "target": target
                })
        return annot
        
    @staticmethod
    def upload_annot_file(apiKey, dataIdentifier, tropyAnnotFile, nkl_route_path):
        """
        Uploads an annotation file from Tropy to Nakala.
        :param apiKey: API key for Nakala
        :param dataIdentifier: Data identifier for Nakala
        :param tropyAnnotFile: Path to the Tropy annotation file
        :param nkl_route_path: The route path of the Nakala instance (test or prod)
        :return: None
        """
        annot_file_open = open(tropyAnnotFile, 'r')
        files = {'file': ('tropy.json', annot_file_open)}
        upload_file_api_url = nkl_route_path + '/datas/uploads'
        Config.uploadsAPIHeaders['X-API-KEY'] = apiKey
        Config.filesAPIHeaders['X-API-KEY'] = apiKey

        url_path_datas = nkl_route_path + Config.nakala_url_datas

        try:
            upload_file_api_response = requests.post(upload_file_api_url, files=files, headers=Config.uploadsAPIHeaders)
            if upload_file_api_response.status_code == 201:
                sha1 = upload_file_api_response.json()['sha1']
                add_file_api_url = url_path_datas + dataIdentifier + '/files'
                data = {
                    'sha1': sha1,
                    'description': Config.ANNOT_FILE_DESCRIPTION
                }
                dataJSON = json.dumps(data)
                add_file_api_response = requests.post(add_file_api_url, headers=Config.filesAPIHeaders, data=dataJSON)
                print(f"Info : annotation file uploaded for data id {dataIdentifier}")
            else:
                print(upload_file_api_response)
        except Exception as err:
            print(f'An error occurred while uploading the Tropy file: {str(err)}')

    @staticmethod
    def get_data_annot_sha1_if_exists(dataMetadataJSON):
        """
        Get the SHA1 of the annotation file in Nakala if it exists.
        :param dataMetadataJSON: JSON metadata for the data
        :return: SHA1 of the annotation file if it exists, else None
        """
        files = dataMetadataJSON.get('files', [])
        annot_sha1 = None
        for file in files:
            json_file = 'tropy.json'
            if file['name'] == json_file and file['description'] == Config.ANNOT_FILE_DESCRIPTION:
                annot_sha1 = file['sha1']
        return annot_sha1

    @staticmethod
    def delete_annot_file(apiKey, dataIdentifier, annot_file_sha1, nkl_route_path):
        """
        Delete an annotation file from Nakala.
        :param apiKey: API key for Nakala
        :param dataIdentifier: Data identifier for Nakala
        :param annot_file_sha1: SHA1 of the annotation file to delete
        :param nkl_route_path: The route path of the Nakala instance (test or prod)
        :return: Response object from the delete request
        """
        url_path = nkl_route_path + Config.nakala_url_datas
        try:
            Config.uploadsAPIHeaders['X-API-KEY'] = apiKey
            nkl_delete_url = f"{url_path}{dataIdentifier}/files/{annot_file_sha1}"
            response = requests.delete(nkl_delete_url, headers=Config.uploadsAPIHeaders)
            if response.status_code == 204:
                print(f'Info : tropy.json file deleted for data id {dataIdentifier}')
            return response
        except Exception as err:
            print(err)
            return None