import requests

class Api():
    def __init__(self, url, headers, key):
        self.url = url 
        self.headers = headers
        self.key = key

    def get(self, request_url, payload, querystring):
        full_url = self.url + request_url
        headers = self.headers
        response = requests.request("GET", full_url, data=payload, headers=headers, params=querystring)
        return response.json()

    def post(self, request_url, payload, querystring):
        full_url = self.url + request_url
        headers = self.headers
        response = requests.request("POST", full_url, data=payload, headers=headers, params=querystring)
        return response.json()