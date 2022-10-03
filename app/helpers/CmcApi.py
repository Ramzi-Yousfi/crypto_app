import os
import json
from pprint import pprint

import requests
class CmcApi:
    def __init__(self):
        self.base_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

        self.parameters = {
            'start': '1',
            'limit': '10',
            'convert': 'EUR'
        }
        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': '4d5214bb-5162-4b82-8b1d-b5f75a1d3dbd'
        }

    def get_all(self):
        """
        The get_all function retrieves all the data from the API and returns it as a list of dictionaries.
        The get_all function is called by other functions to retrieve all the data from their respective endpoints.

        :param self: Access variables that belongs to the class
        :return: The data from the api
        """
        response = requests.get(self.base_url, headers=self.headers, params=self.parameters)
        if response:
            response_json = response.json()
            return response_json['data']
        else :
            raise ValueError('the request return none ')






