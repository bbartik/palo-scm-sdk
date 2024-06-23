import pandas as pd
from .base_processor import BaseProcessor
from scm.scm import ServicesEndpoint

class ServiceProcessor(BaseProcessor):
    def __init__(self, file_path, folder_name):
        super().__init__(file_path)
        self.endpoint = ServicesEndpoint()
        self.folder_name = folder_name

    def process(self):
        df = self.load_csv()
        df.drop(columns=["Location"], inplace=True)

        for index, row in df.iterrows():
            service_name = row['Name']
            protocol = row['Protocol'].lower()
            destination_port = row['Destination Port']
            tags = row['Tags']

            if pd.isna(tags):
                tags = []
            else:
                tags = tags.split(';')

            service_data = {
                "name": service_name,
                "description": "Imported service",
                "protocol": {
                    protocol: {
                        "port": destination_port.strip()
                    }
                },
                "tag": [tag.strip() for tag in tags]
            }


            # Optionally include source_port if not empty
            if pd.notna(row.get('Source Port')):
                service_data["protocol"][protocol]["source_port"] = row['Source Port'].strip()

            self.process_object(self.endpoint, self.folder_name, service_data, service_name, "service")
