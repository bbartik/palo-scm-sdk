import pandas as pd
from .base_processor import BaseProcessor
from scm.scm import SecurityRulesEndpoint

class SecurityRuleProcessor(BaseProcessor):
    def __init__(self, file_path, folder_name):
        super().__init__(file_path)
        self.endpoint = SecurityRulesEndpoint()
        self.folder_name = folder_name

    def process(self):
        df = self.load_csv()
        df.drop(columns=["Location"], inplace=True)

        for index, row in df.iterrows():
            rule_name = row['Name']
            action = row['Action'].lower()
            applications = row['Application'].split(';')
            # categories = row['Category'].split(';')
            # description = row['Description']
            destinations = row['Destination Address'].split(';')
            # destinations_hip = row['Destination HIP'].split(';') if pd.notna(row['Destination HIP']) else []
            from_zones = row['Source Zone'].split(';')
            # log_setting = row['Log Setting']
            # negate_destination = row['Negate Destination'] == 'true'
            # negate_source = row['Negate Source'] == 'true'
            # profile_groups = row['Profile Group'].split(';')
            services = row['Service'].split(';')
            sources = row['Source Address'].split(';')
            # sources_hip = row['Source HIP'].split(';') if pd.notna(row['Source HIP']) else []
            # source_users = row['Source User'].split(';') if pd.notna(row['Source User']) else []
            tags = row['Tags'].split(';') if pd.notna(row['Tags']) else []
            to_zones = row['Destination Zone'].split(';')
            # disabled = row['Disabled'] == 'true'

            security_rule_data = {
                "action": action,
                "application": [app.strip() for app in applications],
                # "category": [cat.strip() for cat in categories],
                "category": ["any"],
                # "description": description,
                "destination": [dest.strip() for dest in destinations],
                # "destination_hip": [hip.strip() for hip in destinations_hip],
                # "disabled": disabled,
                "from": [zone.strip() for zone in from_zones],
                # "log_setting": log_setting,
                "name": rule_name,
                # "negate_destination": negate_destination,
                # "negate_source": negate_source,
                # "profile_setting": {
                #     "group": [group.strip() for group in profile_groups]
                # },
                "service": [service.strip() for service in services],
                "source": [src.strip() for src in sources],
                # "source_hip": [hip.strip() for hip in sources_hip],
                # "source_user": [user.strip() for user in source_users],
                "source_user": ["any"],
                "tag": [tag.strip() for tag in tags],
                "to": [zone.strip() for zone in to_zones]
            }

            self.process_object(self.endpoint, self.folder_name, security_rule_data, rule_name, "security rule")
