#!/bin/bash

# Define the base directory for the file
BASE_DIR="strata_sdk/strata_sdk"
FILE_NAME="scm.py"

# Create the base directory if it doesn't exist
mkdir -p $BASE_DIR

# Path to the file
FILE_PATH="$BASE_DIR/$FILE_NAME"

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

# Template for the BaseEndpoint class
base_endpoint='from ..client import StrataClient
import httpx

class BaseEndpoint:
    def __init__(self, resource):
        self.client = StrataClient()
        self.resource = resource

    def get_all(self, folder):
        endpoint = f"/{self.resource}"
        params = {"folder": folder}
        return self.client.get(endpoint, params=params)

    def create(self, folder, data):
        endpoint = f"/{self.resource}"
        params = {"folder": folder}
        try:
            return self.client.post(endpoint, params=params, data=data)
        except httpx.HTTPStatusError as e:
            print(f"Error: {e.response.status_code} - {e.response.text}")
            return None

    def delete(self, folder, resource_id):
        endpoint = f"/{self.resource}/{resource_id}"
        params = {"folder": folder}
        return self.client.delete(endpoint, params=params)

    def update(self, folder, resource_id, data):
        endpoint = f"/{self.resource}/{resource_id}"
        params = {"folder": folder}
        return self.client.put(endpoint, params=params, data=data)
'

# Write the BaseEndpoint class to the file
echo "$base_endpoint" > $FILE_PATH

# Template for each endpoint class
template='

class ClassNameEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("resource-name")
'

# Create each endpoint class and append to the file
for endpoint in "${endpoints[@]}"; do
    # Convert hyphens to underscores for the class name
    class_name=$(echo "$endpoint" | sed -r 's/(^|-)([a-z])/\U\2/g')
    
    # Replace placeholders in the template
    content=$(echo "$template" | sed "s/ClassName/${class_name}/g" | sed "s/resource-name/${endpoint}/g")
    
    # Append the content to the file
    echo "$content" >> $FILE_PATH
done

echo "File created successfully at $FILE_PATH."
