import os

class BaseProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.debug = os.getenv('SCM_DEBUG', 'False').lower() in ('true', '1', 't')
        self.yes_to_all = False  # Add a flag to track "yes to all"

    def load_csv(self):
        import pandas as pd
        return pd.read_csv(self.file_path)

    def log(self, message):
        if self.debug:
            print(message)

    def prompt_overwrite(self, name):
        if self.yes_to_all:
            return True
        while True:
            response = input(f"Object '{name}' already exists. Do you want to overwrite it? (y/n/yes to all): ").lower()
            if response == 'y':
                return True
            elif response == 'yes to all':
                self.yes_to_all = True
                return True
            elif response == 'n':
                return False

    def process_object(self, endpoint, folder_name, data, object_name, object_type):
        response = endpoint.create(folder_name, data)
        if response is not None and response.status_code == 201:
            print(f"Successfully created {object_type}: {object_name}")
        elif response is not None and response.status_code == 400:
            error_details = response.json().get('_errors', [{}])[0].get('details', {})
            if error_details.get('errorType') == 'Object Already Exists':
                if self.prompt_overwrite(object_name):
                    try:
                        updated_object = endpoint.update(folder_name, data['name'], data)
                        if updated_object is not None and updated_object.status_code == 200:
                            print(f"Successfully updated {object_type}: {object_name}")
                        else:
                            print(f"Failed to update {object_type}: {object_name} - Set SCM_DEBUG to True for more info.")
                    except Exception as update_e:
                        self.log(f"Error: {update_e}")
                        print(f"Failed to update {object_type}: {object_name} - Set SCM_DEBUG to True for more info.")
                else:
                    print(f"Skipping update for {object_type}: {object_name}")
            else:
                print(f"Failed to create {object_type}: {object_name} - Set SCM_DEBUG to True for more info.")
                self.log(f"Error: {response.text if response else 'No response received'}")