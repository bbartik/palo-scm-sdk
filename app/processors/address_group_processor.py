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

            response = self.endpoint.create(self.folder_name, address_group_data)
            if response is not None and response.status_code == 201:
                print(f"Successfully created address group: {group_name}")
            elif response is not None and response.status_code == 400:
                error_details = response.json().get('_errors', [{}])[0].get('details', {})
                if error_details.get('errorType') == 'Object Already Exists':
                    if self.prompt_overwrite(group_name):
                        try:
                            updated_group = self.endpoint.update(self.folder_name, address_group_data['name'], address_group_data)
                            if updated_group is not None and updated_group.status_code == 200:
                                print(f"Successfully updated address group: {group_name}")
                            else:
                                print(f"Failed to update address group: {group_name} - Set SCM_DEBUG to True for more info.")
                        except Exception as update_e:
                            self.log(f"Error: {update_e}")
                            print(f"Failed to update address group: {group_name} - Set SCM_DEBUG to True for more info.")
                    else:
                        print(f"Skipping update for address group: {group_name}")
                else:
                    print(f"Failed to create address group: {group_name} - Set SCM_DEBUG to True for more info.")
                    self.log(f"Error: {response.text if response else 'No response received'}")
