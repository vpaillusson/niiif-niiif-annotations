# -*- encoding: utf-8 -*-

import json
import requests

from tqdm import tqdm
from src.hash import hash_pictures
from src.metadata import Metadata
from src.annotation import Annotation
from src.connection_api import Connection_Nakala
from src.config import Config
from src.output import Output
from src.reorder import Reorder

class Manifest:
    @staticmethod
    #create manifest with annotations
    def create_data_manifest(apiKey, dataIdentifier, dataMetadataJSON, 
                             tropyAnnotFile, formatAnnot, nkl_route_path, searchBaseUrl, method, nkl_route_id):
        """
        It takes a Nakala data identifier, a Nakala API key, 
        and a JSON object containing the metadata of
        the data, and returns a JSON object containing the manifest.
        
        :param apiKey: the API key of the user who is creating the manifest
        :param dataIdentifier: the Nakala identifier of the data 
            (ex: 10.34847/nkl.c1d1w5fj)
        :param dataMetadataJSON: the metadata of the data (the Nakala data)
        :param tropyAnnotFile: the tropy annotation file
        :param formatAnnot: the format of the annotation (plain or html)
        :param nkl_route_path: the route path of the Nakala instance
        :param searchBaseUrl: the route to search service
        :param method: method used to generate annotations
        :param nkl_route_id: route used to generate id of the manifest
        :return: The manifest is being returned.
        """
        
        manifest = None
        Config.filesAPIHeaders['X-API-KEY'] = apiKey
        full_default_jpg = "/full/full/0/default.jpg"
        
        # Open tropy annotation file
        with open(tropyAnnotFile, encoding='utf8') as annot_file:
            annot_file_open = json.loads(annot_file.read())
        
        try:
            # Create variables for storage of canvas, metadata and pdf file
            canvases = []
            pdf_file = [] 

            # Create variable for Nakala metadata
            metadatas = dataMetadataJSON['metas']

            metadata_field = Metadata.create_metadata(metadatas)
        
            title_item = Metadata.get_title(metadatas)
            
            files = dataMetadataJSON['files']
            data_files_total_number = 0

            
            for file in tqdm(files):
                if file['mime_type'] in {'image/tiff', 'image/jpeg'}:
                    data_files_total_number += 1
                    fileName = file['name'] # variable pour la version light et rapide du script. Utilisation du fileName plutôt que du sha1 pour générer le manifest.
                    sha1 = file['sha1']
                    idFile = dataIdentifier + "/" + str(sha1)
                    number_annot = 0

                    url_id = nkl_route_path + Config.nakala_url_iiif + idFile

                    # Check if file is a tiff/jpeg or pdf
                    if file['mime_type'] in {'image/tiff', 'image/jpeg'}:
                        
                        canvasURI = url_id + "/Canvas" 
                        
                        annotations = Annotation.create_annot(annot_file_open, 
                                                                sha1, idFile, 
                                                                number_annot, 
                                                                formatAnnot, 
                                                                nkl_route_path, fileName, method)
                        
                        size_canva = Metadata.get_size_canvas(annot_file_open, 
                                                                sha1)
                        
                        #create canvas
                        canvases_template={
                                "id": canvasURI,
                                "type": "Canvas",
                                "label": {"none": [file["name"]]},
                                "width": size_canva[0],
                                "height": size_canva[1],
                                "items": [
                                    {

                                        "id": url_id +
                                            "/AnnotationPage",
                                        "type": "AnnotationPage",
                                        "items": [
                                            {
                                                "id": url_id + Config.annot_url_arg,

                                                "type": "Annotation",
                                                "motivation": "painting",
                                                "target": canvasURI,
                                                "body": {
                                                    "id": url_id + full_default_jpg,
                                                    "type": "Image",
                                                    "format": "image/jpeg",
                                                    "service": [
                                                        {
                                                            "id": url_id,
                                                            "type": "ImageService3",
                                                            "profile": "level2"
                                                        }
                                                    ]
                                                }
                                            }]
                                    }],
                                "annotations": [
                                    {
                                        "id": url_id + Config.annot_url_arg,
                                        "type": "AnnotationPage",
                                        "items": annotations
                                    }
                                ],
                                "thumbnail": [
                                    {
                                        "id": url_id + full_default_jpg,
                                        "type": "Image",
                                        "service": [
                                            {
                                                "id": url_id,
                                                "type": "ImageService3",
                                                "profile": "level2",
                                            }
                                        ]
                                    }
                                ],
                            }
                        canvases.append(canvases_template)

                    #condition if file is a pdf
                    elif file['mime_type'] in {'application/pdf'}:
                    
                        pdf_file.append(
                            {
                                "id": url_id,
                                "type": "Text",
                                "label": {
                                    "fr": [
                                        "Visualisation PDF"
                                    ]
                                },
                                "format": "application/pdf"
                            }
                        )
                            
                            
            
            # ajout du service search dans les annotations
            # le service search ajouté ici s'appuie par défaut sur le module Omeka-s IIIF annot search développé par Vincent Paillusson (EFEO)
            
            # Définition en paramètre une autre base URL + préfix pour le service search. La valeur par défaut est : 
            #baseUrlIifAnnotsearchEFEO = "https://banyan.efeo.fr/iiif-annot-search"
            
            if searchBaseUrl != "False":
                
                # version 1 de l'APi search
                iiifAnnotSearchService =  {
                        "@context": "http://iiif.io/api/search/1/context.json",
                        "@id": searchBaseUrl+"/"+dataIdentifier, 
                        "profile": "http://iiif.io/api/search/1/search"
                        },
                
                
                '''
                # version 2 de la déclaration de l'api search. Demandé par le validateur IIIF api presentation v3 mais pas accepté par Mirador
                iiifAnnotSearchService =  [
                        {
                        "id": baseUrlIifAnnotsearch+"/"+dataIdentifier,
                        "type": "SearchService2"
                        }
                    ]
                '''

                # l'attribut service n'est affiché que si le paramètre -searchUrl est renseigné lors de la requête 
                manifestData = {
                    "@context": "http://iiif.io/api/presentation/3/context.json",
                    "id": nkl_route_id + Config.nakala_url_data + dataIdentifier,
                    "type": "Manifest",
                    "requiredStatement": {
                        "label": {"fr": ["Attribution"]},
                        "value": {"proprietaire": [dataMetadataJSON["owner"]["name"]]},
                    },
                    "label": {"titre": [title_item]},
                    "service" : iiifAnnotSearchService,  
                    "metadata": metadata_field,
                    "rendering": pdf_file,
                    "items": canvases,
                }
            else:
                # sans propriété service
                manifestData = {
                    "@context": "http://iiif.io/api/presentation/3/context.json",
                    "id": nkl_route_id + Config.nakala_url_data + dataIdentifier,
                    "type": "Manifest",
                    "requiredStatement": {
                        "label": {"fr": ["Attribution"]},
                        "value": {"proprietaire": [dataMetadataJSON["owner"]["name"]]},
                    },
                    "label": {"titre": [title_item]},
                    "metadata": metadata_field,
                    "rendering": pdf_file,
                    "items": canvases,
                }
                

            manifest = json.dumps(manifestData, indent=4)
            #check if manifest is not empty
            if manifest is not None:
                print("Le manifest a été créé")
            else:
                print("Le manifest est vide")
        except Exception as err:
            print(f"Error: {str(err)}")
        return manifest
    
    @staticmethod
    def create_manifest_without_annot(apiKey, dataIdentifier, dataMetadataJSON, 
                                      nkl_route_path, nkl_route_id):
        """
        It takes a Nakala data identifier, a Nakala API key, 
        and a JSON object containing the metadata of
        the data, and returns a JSON object containing the manifest.
        
        :param apiKey: the API key of the user who is creating the manifest
        :param dataIdentifier: the Nakala identifier of the data 
            (ex: 10.34847/nkl.c1d1w5fj)
        :param dataMetadataJSON: the metadata of the data (the Nakala data)
        :param nkl_route_path: the route path of the Nakala instance
        :param nkl_route_id: route used to generate id of the manifest
        :return: The manifest is being returned.
        """

        manifest = None
        Config.filesAPIHeaders['X-API-KEY'] = apiKey
        full_default_jpg = "/full/full/0/default.jpg"

        try:
            # Create variables for storage of canvas, metadata and pdf file
            canvases = []
            pdf_file = [] 

            # Create variable for Nakala metadata
            metadatas = dataMetadataJSON['metas']
            

            metadata_field = Metadata.create_metadata(metadatas)
            # DEBUG
            #print("debug ligne 324 manifest.py")
            #print(metadata_field)
            ## FIN DEBUG
            title_item = Metadata.get_title(metadatas)

            files = dataMetadataJSON['files']
            data_files_total_number = 0

            for file in files:
                if file['mime_type'] in {'image/tiff', 'image/jpeg'}:
                    data_files_total_number += 1

            with tqdm(total=data_files_total_number) as pbar:
                
                for file in files:
                    sha1 = file['sha1']
                    idFile = dataIdentifier + "/" + str(sha1)

                    url_id = nkl_route_path + Config.nakala_url_iiif + idFile
              
                    # Check if file is a tiff/jpeg or pdf
                    if file['mime_type'] in {'image/tiff', 'image/jpeg'}:
                        ## DEBUG
                        #print("debug ligne 348 manifest.py")
                        #print(file['name'])
                        ## FIN DEBUG
                        fileMetadataJSON = None
                        width = 100
                        height = 100
                        '''
                        url_path = nkl_route_path + "/" + dataIdentifier + "/" + str(sha1)
                        url_json = url_path + "/info.json"
                        
                        try:
                            fileMetadata = requests.get(url_json,
                                                        headers=Config.filesAPIHeaders)
                            fileMetadataJSON = fileMetadata.json()
                            width = fileMetadataJSON['width']
                            print( f"width : {width}")
                            height = fileMetadataJSON['height']
                        except Exception as err:
                            print(err)
                        '''
                        canvasURI = url_id + "/Canvas" 

                        # Create canvas
                        canvases_template={
                                "id": canvasURI,
                                "type": "Canvas",
                                "label": {"none": [file["name"]]},
                                "width": width,
                                "height": height,
                                "items": [
                                    {
                                        "id": url_id +
                                            "/AnnotationPage",
                                        "type": "AnnotationPage",
                                        "items": [
                                            {

                                                "id": url_id + Config.annot_url_arg,
                                                "type": "Annotation",
                                                "motivation": "painting",
                                                "target": canvasURI,
                                                "body": {
                                                    "id": url_id + full_default_jpg,
                                                    "type": "Image",
                                                    "format": "image/jpeg",
                                                    "service": [
                                                        {
                                                            "id": url_id,
                                                            "type": "ImageService3",
                                                            "profile": "level2"
                                                        }
                                                    ]
                                                }
                                            }]
                                    }],
                                "thumbnail": [
                                    {
                                        "id": url_id + full_default_jpg,
                                        "type": "Image",
                                        "service": [
                                            {
                                                "id": url_id,
                                                "type": "ImageService3",
                                                "profile": "level2",
                                            }
                                        ]
                                    }
                                ],
                            }
                        canvases.append(canvases_template)
                        ## DEBUG
                        #print("debug ligne 419 manifest.py")
                        #print(canvases)
                        ## FIN DEBUG
                    # Condition if file is a pdf
                    elif file['mime_type'] in {'application/pdf'}:
                        
                        pdf_file.append(
                            {
                                "id": url_id,
                                "type": "Text",
                                "label": {
                                    "fr": [
                                        "Visualisation PDF"
                                    ]
                                },
                                "format": "application/pdf"
                            }
                        )
                        
                        pbar.set_postfix(file=file["name"], refresh=False)
                        pbar.update()
                        
            # @id devrait être modifié pour correspondre à l'URL de téléchargement 
            # du fichier metadata.json sur
            # Nakala (qui contient le SHA1 du fichier) 
            # mais il faudrait pourvoir modifier le fichier une fois déposé
            # sur Nakala, ce qui n'est évidemment pas possible.

            ## DEBUG
            #print("debug ligne 447 manifest.py")
            
            ## FIN DEBUG
            ## il y avait un problème avec la variable dataMetadataJSON["owner"]["name"] qui faisait planter
            ## le script sans renvoyer d'erreur.
            #print("contenu de metadataJson")
            #print(dataMetadataJSON)
            #owner_name = ("Anonyme", dataMetadataJSON["owner"]["name"])[dataMetadataJSON["owner"] != None]
            
            if dataMetadataJSON["owner"] == None:
                owner_name = "Anonyme"
            else:
                owner_name = dataMetadataJSON["owner"]["name"]
             
            
            manifestData = {
                "@context": "http://iiif.io/api/presentation/3/context.json",
                "id": nkl_route_id + Config.nakala_url_data + dataIdentifier,
                "type": "Manifest",
                "requiredStatement": {
                    "label": {"fr": ["Attribution"]},
                    "value": {"proprietaire": [owner_name]},
                },
                "label": {"titre": [title_item]},
                "metadata": metadata_field,
                "rendering": pdf_file,
                "items": canvases,
            }
            
            ## DEBUG
            #print("debug ligne 461 manifest.py")
            #print(manifestData)
            ## FIN DEBUG

            manifest = json.dumps(manifestData, indent=4)
            ## DEBUG
            #print("debug ligne 467 manifest.py")
            #print(manifest)
            ## FIN DEBUG
            # Check if manifest is not empty
            if manifest is not None:
                print("Le manifest a été créé")
            else:
                print("Le manifest est vide")
        except Exception as err:
            print(f"Error: {str(err)}")
        return manifest
    
    @staticmethod
    def upload_manifest_file(apiKey, dataIdentifier, manifest, nkl_route_path, 
                             csv_output):
        files = {'file': ('metadata.json', manifest)}
        upload_file_api_url = nkl_route_path + '/datas/uploads'
        Config.uploadsAPIHeaders['X-API-KEY'] = apiKey
        Config.filesAPIHeaders['X-API-KEY'] = apiKey

        url_path_datas = nkl_route_path + Config.nakala_url_datas
        url_path_data = nkl_route_path + Config.nakala_url_data + str(dataIdentifier) 
        manifestUri = url_path_data.replace("api","")
        try:
            # Upload the file metadata.json to Nakala via l'API /datas/uploads
            upload_file_api_response = requests.post(upload_file_api_url, 
                files=files, headers=Config.uploadsAPIHeaders)
            if upload_file_api_response.status_code == 201:
                
                # retrieve sha1 on the file through Nakala json response
                sha1 = upload_file_api_response.json()['sha1']

                add_file_api_url = url_path_datas + dataIdentifier + '/files'
                data = {
                    'sha1': sha1,
                    'description': Config.MANIFEST_FILE_DESCRIPTION
                }
                dataJSON = json.dumps(data)

                # add file to Nakala resource through API /files
                add_file_api_response = requests.post(add_file_api_url, 
                    headers=Config.filesAPIHeaders, data=dataJSON)
                if add_file_api_response.status_code == 200:
                    data_manifest = url_path_data + '/' + str(sha1)
                    print(f'Manifest file URL for a IIIF viewer : {data_manifest}') 
                    print(f'Manifest URI for validation purpose : {manifestUri}')
                    Output.output_csv(data_manifest, dataIdentifier, csv_output)
                elif add_file_api_response.status_code == 403:
                    print("Erreur 403 : Impossible d'ajouter le fichier à la donnée Nakala. Clé d'API non valide ou utilisateur inconnu")
                elif add_file_api_response.status_code == 401:
                    print("Erreur 401 : Impossible d'ajouter le fichier à la donnée Nakala. Clé d'API manquante ou invalide, compte utilisateur inexistant")
                elif add_file_api_response.status_code == 500:
                    print("Erreur 500 : Impossible d'ajouter le fichier à la donnée Nakala. Erreur lors de l'enregistrement du fichier")
                elif add_file_api_response.status_code == 404:
                    print("Erreur 404 : Impossible d'ajouter le fichier à la donnée Nakala. La donnée n'existe pas ou n'est pas accessible")
                elif add_file_api_response.status_code == 409:
                    print("Erreur 409 : Impossible d'ajouter le fichier à la donnée Nakala. La donnée contient déjà le fichier à ajouter")
                else:
                    print("Impossible d'ajouter le fichier à la donnée Nakala.")
                    print(add_file_api_response)
            elif add_file_api_response.status_code == 403:
                    print("Erreur 403 : Impossible d'uploader le fichier. Clé d'API non valide ou utilisateur inconnu")
            elif add_file_api_response.status_code == 401:
                print("Erreur 401 : Impossible d'uploader le fichier. Clé d'API manquante ou invalide, compte utilisateur inexistant")
            elif add_file_api_response.status_code == 500:
                print("Erreur 500 : Erreur lors de l'enregistrement du fichier")
            else:
                print("Impossible d'uploader le fichier.")
                print(upload_file_api_response)
        except Exception as err:
            print(f'Une erreur est survenue lors de l\'upload du manifest : {str(err)}')

    @staticmethod
    def create_data_manifest_with_annot_if_data_exists(apiKey, dataIdentifier, 
                                                    tropyAnnotFile, formatAnnot,
                                                    nkl_route_path, csv_output, searchBaseUrl,method,nkl_route_id): 

        #response = Connection_Nakala.get_data_metadata(apiKey, dataIdentifier, 
        #                                               nkl_route_path)

        # Connectionto Nakal API 
        try:
            connection = Connection_Nakala(apiKey, nkl_route_path)
            response = connection.get_data_metadata(dataIdentifier)
        except Exception as e:
            print(f"Une erreur s'est produite : {str(e)}")
        finally:
            connection.close()

        #  If connection to API was successful delete manifest.json and tropy.json if they exist in Nakala resource
        if response.status_code == 200:
            dataMetadataJSON = response.json()
            manifest_sha1 = Manifest.get_data_manifest_sha1_if_exists(dataMetadataJSON)
            annotation_file_sha1 = Annotation.get_data_annot_sha1_if_exists(dataMetadataJSON)
            
            if annotation_file_sha1 is not None:
                Annotation.delete_annot_file(apiKey, dataIdentifier, 
                                             annotation_file_sha1, nkl_route_path)
                
            if manifest_sha1 is not None:
                Manifest.delete_manifest(apiKey, dataIdentifier, manifest_sha1, 
                                         nkl_route_path)
            #print("before generating manifest ligne 549 manifest.py")
            manifest = Manifest.create_data_manifest(apiKey, dataIdentifier, 
                dataMetadataJSON, tropyAnnotFile, formatAnnot, nkl_route_path, searchBaseUrl, method, nkl_route_id)
            
            if manifest is not None:
                #print("start manifest upload to Nakala")
                Manifest.upload_manifest_file(apiKey, dataIdentifier, manifest, 
                                            nkl_route_path, csv_output)
                Annotation.upload_annot_file(apiKey,dataIdentifier,tropyAnnotFile,
                                            nkl_route_path)
                list = Reorder.get_files_list(dataIdentifier, apiKey, nkl_route_path)
                Reorder.reorder_list(dataIdentifier, apiKey, nkl_route_path, list)            
            else:
                print("The manifest could not be created")

        else:
            print(response.json()['message'])

    @staticmethod
    def create_data_manifest_without_annot_if_data_exists(apiKey, dataIdentifier, 
                                                    nkl_route_path, csv_output,nkl_route_id):
        
        #response = Connection_Nakala.get_data_metadata(apiKey, dataIdentifier, 
        #                                               nkl_route_path)

        try:
            connection = Connection_Nakala(apiKey, nkl_route_path)
            response = connection.get_data_metadata(dataIdentifier)
        except Exception as e:
            print(f"Une erreur s'est produite : {str(e)}")
        finally:
            connection.close()

        if response.status_code == 200:
            dataMetadataJSON = response.json()
            manifest_sha1 = Manifest.get_data_manifest_sha1_if_exists(dataMetadataJSON)
            if manifest_sha1 is not None:
                Manifest.delete_manifest(apiKey, dataIdentifier, manifest_sha1, 
                                         nkl_route_path)
            print("before generating manifest ligne 586 manifest.py")   
            manifest = Manifest.create_manifest_without_annot(apiKey, dataIdentifier, 
                dataMetadataJSON, nkl_route_path,nkl_route_id)
            
            if manifest is not None:
                print("start manifest upload")
                Manifest.upload_manifest_file(apiKey, dataIdentifier, manifest, 
                                              nkl_route_path, csv_output)
                list = Reorder.get_files_list(dataIdentifier, apiKey, nkl_route_path)
                Reorder.reorder_list(dataIdentifier, apiKey, nkl_route_path, list)
            else:
                print("The manifest could not be created")
        else:
            print(response.json()['message'])

    @staticmethod
    def get_manifest_file_url(apiKey, dataIdentifier, nkl_route_path):
        url_path = nkl_route_path + Config.nakala_url_datas
        url_files = url_path + dataIdentifier + '/files/'
        Config.filesAPIHeaders['X-API-KEY'] = apiKey
        try:
            response = requests.get(url_files, headers=Config.filesAPIHeaders)
            if response.status_code == 200:
                manifest = response.json()
                for files in manifest : 
                    if files['name'] == 'metadata.json' : 
                        sha1 = files['sha1']
                        url = Config.nakala_url_data + dataIdentifier + "/" + sha1
                        #flash("URL: " + url)
                        return url
        except Exception as err:
            print(err)

    @staticmethod    
    # Delete manifest
    def delete_manifest(apiKey, dataIdentifier, sha1, nkl_route_path):
        url_path = nkl_route_path + Config.nakala_url_datas
        try:
            Config.uploadsAPIHeaders['X-API-KEY'] = apiKey
            response = requests.delete(url_path + dataIdentifier + '/files/' + sha1,
                                        headers=Config.uploadsAPIHeaders)
            if response.status_code == 204:
                print(f'Info : metadata.json file deleted for data id {dataIdentifier}')
        except Exception as err:
            print(err)
        return response
    
    @staticmethod
    def get_data_manifest_sha1_if_exists(dataMetadataJSON):
        files = dataMetadataJSON['files']
        manifest_sha1 = None
        for file in files:
            json_file = 'metadata.json'
            if file['name'] == json_file and \
                file['description'] == Config.MANIFEST_FILE_DESCRIPTION:
                manifest_sha1 = file['sha1']
        return manifest_sha1
