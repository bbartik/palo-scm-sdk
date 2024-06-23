import os
import sys

# Ensure the app directory is in the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.processors.address_processor import AddressProcessor
from app.processors.tag_processor import TagProcessor
from app.processors.address_group_processor import AddressGroupProcessor

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    address_file_path = os.path.join(base_dir, 'csv', 'addresses.csv')
    tag_file_path = os.path.join(base_dir, 'csv', 'tags.csv')
    address_group_file_path = os.path.join(base_dir, 'csv', 'address_groups.csv')
    folder_name = os.getenv('FOLDER_NAME', 'ngfw-shared')

    address_processor = AddressProcessor(address_file_path, folder_name)
    tag_processor = TagProcessor(tag_file_path, folder_name)
    address_group_processor = AddressGroupProcessor(address_group_file_path, folder_name)

    # tag_processor.process()
    # address_processor.process()
    address_group_processor.process()

if __name__ == "__main__":
    main()
