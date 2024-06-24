import argparse
import xml.etree.ElementTree as ET
from .processors.tag_processor import TagProcessor
from .processors.address_processor import AddressProcessor

COLOR_MAP = {
    "color24": "Azure Blue",
    "color14": "Black",
    "color3": "Blue",
    "color12": "Blue Gray",
    "color30": "Blue Violet",
    "color16": "Brown",
    "color41": "Burnt Sienna",
    "color25": "Cerulean Blue",
    "color42": "Chestnut",
    "color28": "Cobalt Blue",
    "color5": "Copper",
    "color10": "Cyan",
    "color22": "Forest Green",
    "color15": "Gold",
    "color8": "Gray",
    "color2": "Green",
    "color33": "Lavender",
    "color11": "Light Gray",
    "color9": "Light Green",
    "color13": "Lime",
    "color38": "Magenta",
    "color40": "Mahogany",
    "color19": "Maroon",
    "color27": "Medium Blue",
    "color32": "Medium Rose",
    "color31": "Medium Violet",
    "color26": "Midnight Blue",
    "color17": "Olive",
    "color6": "Orange",
    "color34": "Orchid",
    "color36": "Peach",
    "color7": "Purple",
    "color1": "Red",
    "color39": "Red Violet",
    "color20": "Red-Orange",
    "color37": "Salmon",
    "color35": "Thistle",
    "color23": "Turquoise Blue",
    "color29": "Violet Blue",
    "color4": "Yellow",
    "color21": "Yellow-Orange"
}

def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    return root

def extract_tags(root, base_path, folder_name):
    tags = []
    for tag in root.findall(f".//{base_path}//tag/entry"):
        tag_name = tag.get("name")
        color = tag.find("color").text if tag.find("color") is not None else ''
        comments = tag.find("comments").text if tag.find("comments") is not None else ''
        color_mapped = COLOR_MAP.get(color, None)
        tag_data = {'name': tag_name, 'comments': comments, 'folder': folder_name}
        if color_mapped:
            tag_data['color'] = color_mapped
        tags.append(tag_data)
    return tags

def extract_addresses(root, base_path, folder_name):
    addresses = []
    for address in root.findall(f".//{base_path}//address/entry"):
        address_name = address.get("name")
        address_type = None
        address_value = None

        if address.find("ip-netmask") is not None:
            address_type = "ip_netmask"
            address_value = address.find("ip-netmask").text
        elif address.find("ip-range") is not None:
            address_type = "ip_range"
            address_value = address.find("ip-range").text
        elif address.find("ip-wildcard") is not None:
            address_type = "ip_wildcard"
            address_value = address.find("ip-wildcard").text
        elif address.find("fqdn") is not None:
            address_type = "fqdn"
            address_value = address.find("fqdn").text

        description = address.find("description").text if address.find("description") is not None else ''
        tags = [tag.text for tag in address.findall("tag/member")] if address.find("tag") is not None else []
        
        address_data = {
            'name': address_name,
            address_type: address_value,
            'description': description,
            'tags': tags,
            'folder': folder_name
        }

        addresses.append(address_data)
    return addresses

def process_xml_hierarchy(root):
    hierarchy = {
        "ngfw-shared": {
            "tags": extract_tags(root, "shared", "ngfw-shared"),
            "addresses": extract_addresses(root, "shared", "ngfw-shared"),
        }
    }

    for dg in root.findall(".//device-group/entry"):
        dg_name = dg.get("name")
        hierarchy[dg_name] = {
            "tags": extract_tags(root, f"device-group/entry[@name='{dg_name}']", dg_name),
            "addresses": extract_addresses(root, f"device-group/entry[@name='{dg_name}']", dg_name),
        }

    return hierarchy

def display_hierarchy(hierarchy):
    print("Discovered hierarchy:")
    def print_section(name, level=0):
        print("  " * level + f"- {name}")
        for child in hierarchy.get(name, {}).get('children', []):
            print_section(child, level + 1)

    for section in hierarchy:
        if section != "ngfw-shared":
            print_section(section)
    print_section("ngfw-shared")

def process_section(tags, addresses, folder_name):
    # Process tags
    tag_processor = TagProcessor(folder_name)
    tag_processor.process(tags)

    # Process addresses
    address_processor = AddressProcessor(folder_name)
    address_processor.process(addresses)

def main():
    parser = argparse.ArgumentParser(description="Upload configuration to Strata Cloud Manager")
    parser.add_argument('--xml', type=str, help="Path to the XML file")

    args = parser.parse_args()

    if args.xml:
        root = parse_xml(args.xml)
        hierarchy = process_xml_hierarchy(root)

        display_hierarchy(hierarchy)
        selected_sections = input("Enter the sections you want to process (comma-separated or 'all' for all sections): ").split(',')

        if 'all' in selected_sections:
            selected_sections = hierarchy.keys()

        for section in selected_sections:
            section = section.strip()
            if section in hierarchy:
                process_section(hierarchy[section]['tags'], hierarchy[section]['addresses'], section)
            else:
                print(f"Section '{section}' not found in the hierarchy.")

if __name__ == "__main__":
    main()