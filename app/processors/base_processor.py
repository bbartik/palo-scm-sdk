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