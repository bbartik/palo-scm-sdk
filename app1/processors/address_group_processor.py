import pandas as pd
from .base_processor import BaseProcessor
from scm.scm import AddressGroupEndpoint

class AddressGroupProcessor(BaseProcessor):
    def __init__(self, file_path, folder_name):
        super().__init__(file_path)
        self.endpoint = AddressGroupEndpoint()
        self.folder_name = folder_name

    def process(self):
        df = self.load_csv()
        df.drop(columns=["Location"], inplace=True)

        for index, row in df.iterrows():
            group_name = row['Name']
            members = row['Addresses'].split(';')
            tags = row['Tags'].split(';') if pd.notna(row['Tags']) else []

            address_group_data = {
                "name": group_name,
                "static": [member.strip() for member in members],
                "tags": [tag.strip() for tag in tags] if tags else None
            }

            self.process_object(self.endpoint, self.folder_name, address_group_data, group_name, "address group")

