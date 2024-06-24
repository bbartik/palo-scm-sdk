import pandas as pd
from .base_processor import BaseProcessor
from scm.scm import AddressEndpoint

class AddressProcessor(BaseProcessor):
    def __init__(self, file_path, folder_name):
        super().__init__(file_path)
        self.endpoint = AddressEndpoint()
        self.folder_name = folder_name

    def process(self):
        df = self.load_csv()
        df.drop(columns=["Location"], inplace=True)

        type_mapping = {
            "IP Netmask": "ip_netmask",
            "IP Wildcard": "ip_wildcard",
            "FQDN": "fqdn",
            "IP Range": "ip_range"
        }

        for index, row in df.iterrows():
            name = row['Name']
            address_type = type_mapping.get(row['Type'])
            address_value = row['Address']
            tags = row['Tags']

            if pd.isna(tags):
                tags = []
            else:
                tags = tags.split(';')

            address_data = {
                "name": name,
                "description": "Imported address",
                "tag": [tag.strip() for tag in tags]
            }

            if address_type:
                address_data[address_type] = address_value

            self.process_object(self.endpoint, self.folder_name, address_data, name, "address")
