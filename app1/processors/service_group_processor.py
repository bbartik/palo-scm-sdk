import pandas as pd
from .base_processor import BaseProcessor
from scm.scm import ServiceGroupsEndpoint

class ServiceGroupProcessor(BaseProcessor):
    def __init__(self, file_path, folder_name):
        super().__init__(file_path)
        self.endpoint = ServiceGroupsEndpoint()
        self.folder_name = folder_name

    def process(self):
        df = self.load_csv()
        df.drop(columns=["Location"], inplace=True)

        for index, row in df.iterrows():
            group_name = row['Name']
            services = row['Services'].split(';')
            tags = row['Tags'].split(';') if pd.notna(row['Tags']) else []

            service_group_data = {
                "name": group_name,
                "members": [service.strip() for service in services],
                "tag": [tag.strip() for tag in tags]
            }

            self.process_object(self.endpoint, self.folder_name, service_group_data, group_name, "service group")
