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

            self.process_object(self.endpoint, self.folder_name, tag_data, tag_name, "tag")
