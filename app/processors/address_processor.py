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

            response = self.endpoint.create(self.folder_name, address_data)
            if response is not None and response.status_code == 201:
                print(f"Successfully created address: {name}")
            elif response is not None and response.status_code == 400:
                error_details = response.json().get('_errors', [{}])[0].get('details', {})
                if error_details.get('errorType') == 'Object Already Exists':
                    if self.prompt_overwrite(name):
                        try:
                            updated_address = self.endpoint.update(self.folder_name, address_data['name'], address_data)
                            if updated_address is not None and updated_address.status_code == 200:
                                print(f"Successfully updated address: {name}")
                            else:
                                print(f"Failed to update address: {name} - Set SCM_DEBUG to True for more info.")
                        except Exception as update_e:
                            self.log(f"Error: {update_e}")
                            print(f"Failed to update address: {name} - Set SCM_DEBUG to True for more info.")
                    else:
                        print(f"Skipping update for address: {name}")
                else:
                    print(f"Failed to create address: {name} - Set SCM_DEBUG to True for more info.")
                    self.log(f"Error: {response.text if response else 'No response received'}")
