from .base_processor import BaseProcessor
from scm.scm import TagsEndpoint  # Import the TagsEndpoint from your SCM SDK

class TagProcessor(BaseProcessor):
    def __init__(self, folder_name):
        super().__init__(folder_name)
        self.endpoint = TagsEndpoint()  # Initialize the endpoint

    def process(self, tags):
        for tag in tags:
            response = self.endpoint.create(tag['folder'], tag)
            if response is not None and response.status_code == 201:
                print(f"Successfully created tag: {tag['name']}")
            elif response is not None and response.status_code == 400 and "Object already exists" in response.text:
                print(f"Tag {tag['name']} already exists.")
            else:
                print(f"Failed to create tag: {tag['name']} - {response.text}")
