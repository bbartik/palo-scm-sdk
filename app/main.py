import os
import pandas as pd
from scm.scm import AddressEndpoint, TagsEndpoint

def main():

    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Load CSV files
    addresses_file_path = os.path.join(base_dir, 'csv', 'addresses.csv')
    tags_file_path = os.path.join(base_dir, 'csv', 'tags.csv')
    addresses_df = pd.read_csv(addresses_file_path)
    tags_df = pd.read_csv(tags_file_path)

    # Remove the "Location" field
    addresses_df.drop(columns=["Location"], inplace=True)
    tags_df.drop(columns=["Location"], inplace=True)

    # Initialize the endpoints
    folder_name = "ngfw-shared"
    address_endpoint = AddressEndpoint()
    tags_endpoint = TagsEndpoint()

    # Upload tags from tags.csv
    for index, row in tags_df.iterrows():
        tag_name = row['Name']
        tag_data = {"name": tag_name.strip()}
        
        if pd.notna(row.get('Color')):
            tag_data["color"] = row.get('Color').strip()
        if pd.notna(row.get('Comments')):
            tag_data["comments"] = row.get('Comments').strip()

        try:
            created_tag = tags_endpoint.create(folder_name, tag_data)
            if created_tag:
                print(f"Successfully created tag: {tag_name}")
        except httpx.HTTPStatusError as e:
            print(f"Error: Object name:{tag_name} already exists")
        except Exception as e:
            print(f"Error: {e}")
            print(f"Failed to create tag: {tag_name}")

    # Type mapping
    type_mapping = {
        "IP Netmask": "ip_netmask",
        "IP Wildcard": "ip_wildcard",
        "FQDN": "fqdn",
        "IP Range": "ip_range"
    }

    # Iterate through the rows of the addresses DataFrame to create addresses
    for index, row in addresses_df.iterrows():
        name = row['Name']
        address_type = type_mapping.get(row['Type'])
        address_value = row['Address']
        tags = row['Tags']

        # Skip if tags are NaN
        if pd.isna(tags):
            tags = []
        else:
            tags = tags.split(';')

        # Prepare the address object
        address_data = {
            "name": name,
            "description": "Imported address",
            "tag": [tag.strip() for tag in tags]
        }

        if address_type:
            address_data[address_type] = address_value

        try:
            # Create the address object
            created_address = address_endpoint.create(folder_name, address_data)
            if created_address:
                print(f"Successfully created address: {name}")
        except httpx.HTTPStatusError as e:
            print(f"Error: Object name:{name} already exists")
        except Exception as e:
            print(f"Error: {e}")
            print(f"Failed to create address: {name}")



if __name__ == "__main__":
    main()