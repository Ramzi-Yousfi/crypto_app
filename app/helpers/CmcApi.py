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
        response = requests.get(self.base_url, headers=self.headers, params=self.parameters)
        if response:
            response_json = response.json()
            return response_json['data']
        else :
            raise ValueError('the request return none ')






