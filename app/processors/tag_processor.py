import pandas as pd
from .base_processor import BaseProcessor
from scm.scm import TagsEndpoint

class TagProcessor(BaseProcessor):
    def __init__(self, file_path, folder_name):
        super().__init__(file_path)
        self.endpoint = TagsEndpoint()
        self.folder_name = folder_name

    def process(self):
        df = self.load_csv()
        df.drop(columns=["Location"], inplace=True)

        for index, row in df.iterrows():
            tag_name = row['Name']
            tag_data = {"name": tag_name.strip()}

            if pd.notna(row.get('Color')):
                tag_data["color"] = row.get('Color').strip()
            if pd.notna(row.get('Comments')):
                tag_data["comments"] = row.get('Comments').strip()

            response = self.endpoint.create(self.folder_name, tag_data)
            if response is not None and response.status_code == 201:
                print(f"Successfully created tag: {tag_name}")
            elif response is not None and response.status_code == 400:
                error_details = response.json().get('_errors', [{}])[0].get('details', {})
                if error_details.get('errorType') == 'Object Already Exists':
                    if self.prompt_overwrite(tag_name):
                        try:
                            updated_tag = self.endpoint.update(self.folder_name, tag_data['name'], tag_data)
                            if updated_tag is not None and updated_tag.status_code == 200:
                                print(f"Successfully updated tag: {tag_name}")
                            else:
                                print(f"Failed to update tag: {tag_name} - Set SCM_DEBUG to True for more info.")
                        except Exception as update_e:
                            self.log(f"Error: {update_e}")
                            print(f"Failed to update tag: {tag_name} - Set SCM_DEBUG to True for more info.")
                    else:
                        print(f"Skipping update for tag: {tag_name}")
                else:
                    print(f"Failed to create tag: {tag_name} - Set SCM_DEBUG to True for more info.")
                    self.log(f"Error: {response.text if response else 'No response received'}")