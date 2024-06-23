import os
import sys

# Ensure the app directory is in the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.processors.tag_processor import TagProcessor
from app.processors.address_processor import AddressProcessor
from app.processors.address_group_processor import AddressGroupProcessor
from app.processors.service_processor import ServiceProcessor
from app.processors.service_group_processor import ServiceGroupProcessor


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    tag_file_path = os.path.join(base_dir, 'csv', 'tags.csv')
    address_file_path = os.path.join(base_dir, 'csv', 'addresses.csv')
    address_group_file_path = os.path.join(base_dir, 'csv', 'address_groups.csv')
    service_file_path = os.path.join(base_dir, 'csv', 'services.csv')
    service_group_file_path = os.path.join(base_dir, 'csv', 'service_groups.csv')

    folder_name = os.getenv('FOLDER_NAME', 'ngfw-shared')

    tag_processor = TagProcessor(tag_file_path, folder_name)
    address_processor = AddressProcessor(address_file_path, folder_name)
    address_group_processor = AddressGroupProcessor(address_group_file_path, folder_name)
    service_processor = ServiceProcessor(service_file_path, folder_name)
    service_group_processor = ServiceGroupProcessor(service_group_file_path, folder_name)

    tag_processor.process()
    address_processor.process()
    address_group_processor.process()
    service_processor.process()
    service_group_processor.process()

if __name__ == "__main__":
    main()
