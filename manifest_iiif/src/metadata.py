from src.hash import hash_pictures


class Metadata:
    @staticmethod
    def create_metadata(metadatas):
        """
        Returns a list of dictionaries containing the metadata of the resource.
        :param metadatas: Nakala metadatas of the resource, extracted from Nakala API
        :return: List of metadata dictionaries
        """
        metadata = []

        for meta in metadatas:
            # Extract property name without "purl.org/"
            property_name = meta['propertyUri'].split('/')[-1].replace("terms#","").capitalize()
            '''
            if not meta['value']:
                metadata.append({"label": property_name, "value": "Anonyme"})
            else:
                if "fullName" in meta['value']:
                    value = meta['value']['fullName']
                else:
                    value = meta['value']
                metadata.append({"label": property_name, "value": value})
            '''
            if  meta['value']:
                if "fullName" in meta['value']:
                    value = meta['value']['fullName']
                else:
                    value = meta['value']
                metadata.append({
                    "label":{"en":[property_name]},
                    "value":{"none":[value]} 
                    })
                
        return metadata

    @staticmethod
    def get_title(metadatas):
        """
        Returns the title of the resource.
        :param metadatas: Nakala metadatas of the resource, extracted from Nakala API
        :return: the title of the resource
        """
        for meta in metadatas:
            if meta['propertyUri'].endswith("title"):
                return meta['value']

    @staticmethod
    def get_size_canvas(annot_file_open, sha1):
        """
        Returns the size of the canvas.
        :param annot_file_open: JSON file of tropy
        :param sha1: sha1 of image
        :return: Tuple containing the width and height of the canvas
        """
        for i in annot_file_open["@graph"]:
            for p in i["photo"]:
                filename_path = p.get("path")

                if filename_path:
                    hash_file = hash_pictures(filename_path)
                    if hash_file == sha1:
                        width_canva = p.get("width")
                        height_canva = p.get("height")
                        return width_canva, height_canva

        return None, None
