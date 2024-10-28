from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from markdown2 import markdown

credential = DefaultAzureCredential()

subscription_id = 'your_subscription_id'
resource_client = ResourceManagementClient(credential, subscription_id)
compute_client = ComputeManagementClient(credential, subscription_id)
network_client = NetworkManagementClient(credential, subscription_id)

app_names = ["VP", "HighNat", "NVP", "IVP", "INVP", "5GC"]

def get_resource_groups_with_apps():
    resource_groups = resource_client.resource_groups.list()
    app_data = {}
    
    for app in app_names:
        app_data[app] = {"firewall": "No", "ipv6": "No", "fastpath": "No", "psat_guest_rg": "No", "pta_subnet": "No", "pe_subnet": "No"}
        for rg in resource_groups:
            if app.lower() in rg.name.lower():
                if "psat" in rg.name.lower():
                    app_data[app]["psat_guest_rg"] = "Yes"
                
                vms = compute_client.virtual_machines.list(rg.name)
                for vm in vms:
                    if 'fw' in vm.name.lower():
                        app_data[app]["firewall"] = "Yes"
                    if vm.network_profile and any(ip_config for nic in vm.network_profile.network_interfaces for ip_config in nic.ip_configurations if ip_config.public_ip_address and "ipv6" in ip_config.public_ip_address.ip_version):
                        app_data[app]["ipv6"] = "Yes"
                    if vm.additional_capabilities and vm.additional_capabilities.fastpath:
                        app_data[app]["fastpath"] = "Yes"
                
                subnets = network_client.subnets.list(rg.name, rg.name + '-vnet')  # Assuming the naming convention of the VNet matches RG
                for subnet in subnets:
                    if "pta" in subnet.name.lower():
                        app_data[app]["pta_subnet"] = "Yes"
                    if "pe" in subnet.name.lower():
                        app_data[app]["pe_subnet"] = "Yes"
    
    return app_data

def generate_markdown_table(app_data):
    headers = ["Features", *app_names]
    features = [
        "MT Deployment", "Firewalls", "IPv6 Available", "FastPath Enabled", "PSAT Guest RG", "PTA Subnet", "PE Subnet"
    ]
    
    table = "| " + " | ".join(headers) + " |\n"
    table += "| " + " | ".join(["---"] * len(headers)) + " |\n"

    for feature in features:
        row = [feature]
        for app in app_names:
            if feature == "Firewalls":
                row.append(app_data[app]["firewall"])
            elif feature == "IPv6 Available":
                row.append(app_data[app]["ipv6"])
            elif feature == "FastPath Enabled":
                row.append(app_data[app]["fastpath"])
            elif feature == "PSAT Guest RG":
                row.append(app_data[app]["psat_guest_rg"])
            elif feature == "PTA Subnet":
                row.append(app_data[app]["pta_subnet"])
            elif feature == "PE Subnet":
                row.append(app_data[app]["pe_subnet"])
            else:
                row.append("Yes")  # Replace with actual logic for other features
        table += "| " + " | ".join(row) + " |\n"
    
    return table

def publish_to_wiki(markdown_content):
    personal_access_token = 'your_personal_access_token'
    organization_url = 'https://dev.azure.com/your_organization'

    credentials = BasicAuthentication('', personal_access_token)
    connection = Connection(base_url=organization_url, creds=credentials)

    wiki_client = connection.clients.get_wiki_client()

    project = 'your_project_name'
    wiki_identifier = 'your_wiki_identifier'
    page_path = '/App-Report'

    wiki_client.create_or_update_page(
        project=project,
        wiki_identifier=wiki_identifier,
        path=page_path,
        content=markdown(markdown_content),
        version=None,
    )

if __name__ == "__main__":
    app_data = get_resource_groups_with_apps()
    markdown_content = generate_markdown_table(app_data)
    publish_to_wiki(markdown_content)
