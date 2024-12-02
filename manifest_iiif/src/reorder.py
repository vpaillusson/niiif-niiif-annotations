'''
This class reorder files in Nakala ressources in order for the manifest metadata.json 
file to be on top of the ressource's files.
It is necessary if we want that the manifest id with a syntax like https://nakala.fr/data/{id_nakala}
redirects to https://api.nakala.fr/data/{id_nakala}/{manifest_sha1}
this redirection is a mecanism allowed by Nakala for legacy functionality purpose.
We use it in this script to generate a valid manifest id (which should be equivalent to the uri of the manifest)
'''
import requests
import json
from src.config import Config

class Reorder:
    
    @staticmethod
    def get_files_list(nakala_id, apikey, nkl_route_path):
        identifiant = nakala_id
        base_url = nkl_route_path+Config.nakala_url_datas
        url = base_url+identifiant
        
        session = requests.Session()
        session.headers.update({'X-API-KEY': apikey})
        response = session.get(url)
        list = {}
        list_files = {}
        if response.status_code == 200:
            data = response.json()
            #print(json.dumps(data, indent=2))  # Pretty-print the JSON response
            list_files = json.loads(json.dumps(data)) # récupère les données json sous forme de dictionnaire python
            list = list_files["files"].copy() # copie dans un nouveau dictionnaire uniquement le smétadonnées de fichiers
            #print(list)
            return list
        else:
            print(f"Error: {response.status_code}")
            
    @staticmethod        
    def reorder_list(nakala_id, apikey, nkl_route_path, list):
        # récupère les informations sur le fichier metadata.json dans un nouveau dict manifest_info
        # supprime les informations du fichier metadata.json du dict list
        
        for i in range(len(list)):

                #print(f"valeur de i = {i} et valeur de list length = {len(list)}")
                if (list[i]["name"] == "metadata.json"):
                    #print(file)
                    manifest_info = list[i].copy() # copie du sous dictionnaire de métadonnées du fichier de manifest
                
        new_list = [] # création d'une liste vide
        new_list.append(manifest_info) # ajout des objets dict à la liste

        for i in range(len(list)):
            if not (list[i]["name"] == "metadata.json"):
                new_list.append(list[i])
        new_list = { "files" : new_list} # ajout de la nouvelle liste comme valeur de la clé "files" de métadonnes json 
        #attendue par Nakala
        #print(new_list)
        ordered_list = json.dumps(new_list) # conversion en json
        updateAPIHeaders = {
        'accept': 'application/json',
        'X-API-KEY': apikey,
        'Content-Type': 'application/json'
            }
        base_url = nkl_route_path+Config.nakala_url_datas
        url = base_url+nakala_id
        #print(url)
        try:
            update_response = requests.put(url, headers=updateAPIHeaders, data=ordered_list)
            if update_response.status_code == 204:
                print("la liste des fichiers a été modifiée")
            else:
                print(update_response.status_code)
        except Exception as err:
            print(f'Une erreur est survenue lors de la mise à jour de la ressource : {str(err)}') 