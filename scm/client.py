import httpx
from .auth import get_headers
from .config import BASE_URL

class StrataClient:
    def __init__(self):
        headers = get_headers()
        self.client = httpx.Client(base_url=BASE_URL, headers=headers)

    def get(self, endpoint, params=None):
        response = self.client.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint, params=None, data=None):
        response = self.client.post(endpoint, params=params, json=data)
        response.raise_for_status()
        return response.json()

    def delete(self, endpoint, params=None):
        response = self.client.delete(endpoint, params=params)
        response.raise_for_status()
        return response.json()

    def put(self, endpoint, params=None, data=None):
        response = self.client.put(endpoint, params=params, json=data)
        response.raise_for_status()
        return response.json()
