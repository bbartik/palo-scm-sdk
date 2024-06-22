#!/bin/bash

# Define the base directory for the endpoints
BASE_DIR="strata_sdk/strata_sdk/endpoints"

# Create the base directory if it doesn't exist
mkdir -p $BASE_DIR

# Create the __init__.py file in the endpoints directory
touch $BASE_DIR/__init__.py

# List of endpoint names
endpoints=(
    "address-groups"
    "addresses"
    "anti-spyware-profiles"
    "anti-spyware-signatures"
    "application-filters"
    "application-groups"
    "app-override-rules"
    "applications"
    "authentication-portals"
    "authentication-profiles"
    "authentication-rules"
    "authentication-sequences"
    "auto-tag-actions"
    "bandwidth-allocations"
    "certificate-profiles"
    "certificates"
    "config-versions"
    "dns-security-profiles"
    "decryption-exclusions"
    "decryption-profiles"
    "decryption-rules"
    "dynamic-user-groups"
    "external-dynamic-lists"
    "file-blocking-profiles"
    "hip-objects"
    "hip-profiles"
    "http-header-profiles"
    "ike-crypto-profiles"
    "ike-gateways"
    "ipsec-crypto-profiles"
    "ipsec-tunnels"
    "post-sse-config-v-1-enable"
    "internal-dns-servers"
    "kerberos-server-profiles"
    "ldap-server-profiles"
    "license-types"
    "local-user-groups"
    "local-users"
    "locations"
    "mfa-servers"
    "mobile-agent-agent-profiles"
    "ocsp-responder"
    "profile-groups"
    "qos-policy-rules"
    "qos-profiles"
    "quarantined-devices"
    "radius-server-profiles"
    "regions"
    "remote-networks"
    "saml-server-profiles"
    "scep-profiles"
    "schedules"
    "security-rules"
    "service-connection-groups"
    "bgp-routing"
    "service-connections"
    "service-groups"
    "services"
    "tacacs-server-profiles"
    "tls-service-profiles"
    "tags"
    "traffic-steering-rules"
    "trusted-certificate-authorities"
    "url-access-profiles"
    "url-categories"
    "url-filtering-categories"
    "vulnerability-protection-profiles"
    "vulnerability-protection-signatures"
    "wildfire-anti-virus-profiles"
)

# Template for each endpoint file
template='from .base_endpoint import BaseEndpoint

class ClassNameEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("resource-name")
'

# Create a file for each endpoint
for endpoint in "${endpoints[@]}"; do
    # Convert hyphens to underscores for the class name
    class_name=$(echo "$endpoint" | sed -r 's/(^|-)([a-z])/\U\2/g')
    class_name_file=$(echo "$endpoint" | sed 's/-/_/g')
    
    # Replace placeholders in the template
    content=$(echo "$template" | sed "s/ClassName/${class_name}/g" | sed "s/resource-name/${endpoint}/g")
    
    # Write the content to the file
    echo "$content" > "${BASE_DIR}/${class_name_file}.py"
    
    # Append import statement to __init__.py
    echo "from .${class_name_file} import ${class_name}Endpoint" >> "$BASE_DIR/__init__.py"
done

echo "Files created successfully."
