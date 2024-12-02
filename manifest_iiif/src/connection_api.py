import requests
from src.config import Config

class Connection_Nakala:
    def __init__(self, apiKey, nkl_route_path):
        self.apiKey = apiKey
        self.nkl_route_path = nkl_route_path
        self.session = requests.Session()
        self.session.headers.update({'X-API-KEY': apiKey})

    def get_data_metadata(self, dataIdentifier):
        """
        Returns status code of the request to Nakala API
        :param dataIdentifier: the identifier of the resource
        :return: the status code of the request to Nakala API
        """
        # Create the url
        url_request = self.nkl_route_path + Config.nakala_url_datas + dataIdentifier

        try:
            # The response could be an error message
            response = self.session.get(url_request)
            return response
        except Exception as err:
            print(err)
            return None  

    def close(self):
        self.session.close()
