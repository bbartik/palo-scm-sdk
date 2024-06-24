from .base_processor import BaseProcessor
from scm.scm import AddressEndpoint  # Import the AddressesEndpoint from your SCM SDK

class AddressProcessor(BaseProcessor):
    def __init__(self, folder_name):
        super().__init__(folder_name)
        self.endpoint = AddressEndpoint()  # Initialize the endpoint

    def process(self, addresses):
        for address in addresses:
            response = self.endpoint.create(address['folder'], address)
            if response is not None and response.status_code == 201:
                print(f"Successfully created address: {address['name']}")
            elif response is not None and response.status_code == 400 and "Object already exists" in response.text:
                print(f"Address {address['name']} already exists.")
            else:
                print(f"Failed to create address: {address['name']} - {response.text}")
