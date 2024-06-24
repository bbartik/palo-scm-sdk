import os

class BaseProcessor:
    def __init__(self, folder_name):
        self.folder_name = folder_name

    def log(self, message):
        if os.getenv('SCM_DEBUG', 'False').lower() in ('true', '1', 't'):
            print(message)
