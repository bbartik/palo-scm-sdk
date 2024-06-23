from .client import StrataClient
import httpx
import os

DEBUG = os.getenv('SCM_DEBUG', 'False').lower() in ('true', '1', 't')

class BaseEndpoint:
    def __init__(self, resource):
        self.client = StrataClient()
        self.resource = resource


    def get_all(self, folder):
        endpoint = f"/{self.resource}"
        params = {"folder": folder}
        return self.client.get(endpoint, params=params)

    def get_by_name(self, folder, name):
        endpoint = f"/{self.resource}"
        params = {"folder": folder, "name": name}
        return self.client.get(endpoint, params=params)

    def get_by_id(self, folder, resource_id):
        endpoint = f"/{self.resource}/{resource_id}"
        params = {"folder": folder}
        return self.client.get(endpoint, params=params)

    def create(self, folder, data):
        endpoint = f"/{self.resource}"
        params = {"folder": folder}
        try:
            response = self.client.post(endpoint, params=params, json=data)
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            if os.getenv('SCM_DEBUG', 'False').lower() in ('true', '1', 't'):
                print(f"Error: {e.response.status_code} - {e.response.json()}")
            return e.response

    def update(self, folder, object_name, data):
        # Fetch the UUID of the object to update
        uuid_response = self.client.get(f"/{self.resource}", params={"name": object_name, "folder": folder})
        if uuid_response:
            uuid = uuid_response.get('id')  # Adjust the key if needed
            if uuid:
                endpoint = f"/{self.resource}/{uuid}"
                params = {"folder": folder}
                try:
                    response = self.client.put(endpoint, params=params, json=data)
                    response.raise_for_status()
                    return response
                except httpx.HTTPStatusError as e:
                    if os.getenv('SCM_DEBUG', 'False').lower() in ('true', '1', 't'):
                        print(f"Error: {e.response.status_code} - {e.response.json()}")
                    return e.response
            else:
                print(f"UUID not found in response for object: {object_name}")
                if os.getenv('SCM_DEBUG', 'False').lower() in ('true', '1', 't'):
                    print(f"Error: UUID not found in response: {uuid_response}")
                return None
        else:
            print(f"Failed to find UUID for object: {object_name}")
            if os.getenv('SCM_DEBUG', 'False').lower() in ('true', '1', 't'):
                print(f"Error: No response received")
            return None

    def delete(self, folder, resource_id):
        endpoint = f"/{self.resource}/{resource_id}"
        params = {"folder": folder}
        try:
            return self.client.delete(endpoint, params=params)
        except httpx.HTTPStatusError as e:
            error_message = e.response.json()
            if DEBUG:
                print(f"Error: {e.response.status_code} - {error_message}")
            return None


class AddressGroupEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("address-groups")

    def remove_member(self, folder, group_id, member):
        endpoint = f"/{self.resource}/{group_id}"
        params = {"folder": folder}
        group = self.client.get(endpoint, params=params)

        # Remove member from static or dynamic list
        if "static" in group and member in group["static"]:
            group["static"].remove(member)
        if "dynamic" in group and member in group["dynamic"]["filter"]:
            group["dynamic"]["filter"] = group["dynamic"]["filter"].replace(member, "").strip()

        try:
            return self.client.put(endpoint, params=params, data=group)
        except httpx.HTTPStatusError as e:
            print(f"Error: {e.response.status_code} - {e.response.text}")
            return None

    def add_member(self, folder, group_id, member, is_static=True):
        endpoint = f"/{self.resource}/{group_id}"
        params = {"folder": folder}
        group = self.client.get(endpoint, params=params)

        # Add member to static or dynamic list
        if is_static:
            if "static" not in group:
                group["static"] = []
            group["static"].append(member)
        else:
            if "dynamic" not in group:
                group["dynamic"] = {"filter": ""}
            if group["dynamic"]["filter"]:
                group["dynamic"]["filter"] += f" or {member}"
            else:
                group["dynamic"]["filter"] = member

        try:
            return self.client.put(endpoint, params=params, data=group)
        except httpx.HTTPStatusError as e:
            print(f"Error: {e.response.status_code} - {e.response.text}")
            return None

class AddressEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("addresses")


class AntiSpywareProfilesEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("anti-spyware-profiles")


class AntiSpywareSignaturesEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("anti-spyware-signatures")


class ApplicationFiltersEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("application-filters")


class ApplicationGroupsEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("application-groups")


class AppOverrideRulesEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("app-override-rules")


class ApplicationsEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("applications")


class AuthenticationPortalsEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("authentication-portals")


class AuthenticationProfilesEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("authentication-profiles")


class AuthenticationRulesEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("authentication-rules")


class AuthenticationSequencesEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("authentication-sequences")


class AutoTagActionsEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("auto-tag-actions")


class BandwidthAllocationsEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("bandwidth-allocations")


class CertificateProfilesEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("certificate-profiles")


class CertificatesEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("certificates")


class ConfigVersionsEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("config-versions")


class DnsSecurityProfilesEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("dns-security-profiles")


class DecryptionExclusionsEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("decryption-exclusions")


class DecryptionProfilesEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("decryption-profiles")


class DecryptionRulesEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("decryption-rules")


class DynamicUserGroupsEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("dynamic-user-groups")


class ExternalDynamicListsEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("external-dynamic-lists")


class FileBlockingProfilesEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("file-blocking-profiles")


class HipObjectsEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("hip-objects")


class HipProfilesEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("hip-profiles")


class HttpHeaderProfilesEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("http-header-profiles")


class IkeCryptoProfilesEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("ike-crypto-profiles")


class IkeGatewaysEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("ike-gateways")


class IpsecCryptoProfilesEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("ipsec-crypto-profiles")


class IpsecTunnelsEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("ipsec-tunnels")


class PostSseConfigV1EnableEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("post-sse-config-v-1-enable")


class InternalDnsServersEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("internal-dns-servers")


class KerberosServerProfilesEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("kerberos-server-profiles")


class LdapServerProfilesEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("ldap-server-profiles")


class LicenseTypesEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("license-types")


class LocalUserGroupsEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("local-user-groups")


class LocalUsersEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("local-users")


class LocationsEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("locations")


class MfaServersEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("mfa-servers")


class MobileAgentAgentProfilesEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("mobile-agent-agent-profiles")


class OcspResponderEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("ocsp-responder")


class ProfileGroupsEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("profile-groups")


class QosPolicyRulesEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("qos-policy-rules")


class QosProfilesEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("qos-profiles")


class QuarantinedDevicesEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("quarantined-devices")


class RadiusServerProfilesEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("radius-server-profiles")


class RegionsEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("regions")


class RemoteNetworksEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("remote-networks")


class SamlServerProfilesEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("saml-server-profiles")


class ScepProfilesEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("scep-profiles")


class SchedulesEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("schedules")


class SecurityRulesEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("security-rules")


class ServiceConnectionGroupsEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("service-connection-groups")


class BgpRoutingEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("bgp-routing")


class ServiceConnectionsEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("service-connections")


class ServiceGroupsEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("service-groups")


class ServicesEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("services")


class TacacsServerProfilesEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("tacacs-server-profiles")


class TlsServiceProfilesEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("tls-service-profiles")


class TagsEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("tags")


class TrafficSteeringRulesEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("traffic-steering-rules")


class TrustedCertificateAuthoritiesEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("trusted-certificate-authorities")


class UrlAccessProfilesEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("url-access-profiles")


class UrlCategoriesEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("url-categories")


class UrlFilteringCategoriesEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("url-filtering-categories")


class VulnerabilityProtectionProfilesEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("vulnerability-protection-profiles")


class VulnerabilityProtectionSignaturesEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("vulnerability-protection-signatures")


class WildfireAntiVirusProfilesEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__("wildfire-anti-virus-profiles")
