import argparse
import json
import os
from pprint import pprint

from azure_storage_blob import BlobServiceClient
from dni_client_helper import (
    DNIClient,
    SaBlobClient,
    get_avpn_id,
    get_client_id,
    get_reservation_id,
    get_topo_id,
    get_cn_related_ids,
    create_cn,
    create_cn_only,
    assign_loc,
    update_reach,
    create_topo,
    create_avpns,
    delete_avpns,
    topo_poll,
)


def load_config():
    """Load configuration from the 'access.json' file."""
    with open("access.json", "r") as config_file:
        return json.load(config_file)


def initialize_clients(config_param):
    """Initialize clients using the configuration parameters."""
    tenant_id = os.getenv("tenant_id")
    app_id = os.getenv("app_id")
    passwd = os.getenv("passwd")
    account_id = os.getenv("account_id")
    rm_url = os.getenv("rm_url")
    sa_connect_str = os.getenv("sa_connect_str")

    print(f"Tenant ID: {tenant_id}")
    print(f"App ID: {app_id}")
    print(f"Password: {passwd}")
    print(f"Account ID: {account_id}")
    print(f"RM URL: {rm_url}")
    print(f"SA Connection String: {sa_connect_str}")

    dni_client = DNIClient(
        base_url=rm_url,
        client_id=app_id,
        client_secret=passwd,
        tenant_id=tenant_id,
        scope="api://df62135d-2ede-4bac-9465-a36750479690/.default",
    )
    sa_blob_client = SaBlobClient(sa_connect_str=sa_connect_str)
    return dni_client, sa_blob_client


def get_staging_client(dni_client, account_id, client_name):
    """Get the staging client details."""
    clients = dni_client.get_resources(f"/accounts/{account_id}/resources/clients")[
        "result"
    ]
    stg_client = next(
        client for client in clients if client["name"] == client_name
    )
    print(json.dumps(stg_client, indent=4))
    return stg_client["id"]


def get_bandwidth_reservation(dni_client, account_id, service_provider_name):
    """Get bandwidth reservation details."""
    reservs = dni_client.get_resources(
        f"/accounts/{account_id}/resources/reservations"
    )["result"]
    bw_reserv = next(
        reserv
        for reserv in reservs
        if reserv["serviceProviderName"] == service_provider_name
    )
    print("BW Reservation:")
    pprint(json.loads(json.dumps(bw_reserv, indent=4)))
    return bw_reserv


def list_network_assets(sa_blob_client, container_name):
    """List network assets."""
    for blob in sa_blob_client.get_blob_list(container_name):
        if "avpns" in blob["name"] or "itaom" in blob["name"]:
            print(blob["name"])


def create_cloud_node(dni_client, sa_blob_client, account_id, cn_container_name, cn_blob_name):
    """Create a cloud node."""
    print(f"Creating cloud node with {cn_blob_name}...")
    return create_cn(dni_client, sa_blob_client, account_id, cn_container_name, cn_blob_name)


def assign_location(dni_client, sa_blob_client, account_id, cn_container_name, loc_blob_name, client_id, cn_id):
    """Assign a location."""
    print(f"Assigning location using {loc_blob_name}...")
    return assign_loc(dni_client, sa_blob_client, account_id, cn_container_name, loc_blob_name, client_id, cn_id)


def update_reachability(dni_client, sa_blob_client, cn_container_name, reach_blob_name, client_id, cn_id):
    """Update reachability."""
    print(f"Updating reachability using {reach_blob_name}...")
    return update_reach(dni_client, sa_blob_client, cn_container_name, reach_blob_name, client_id, cn_id)


def create_topology_vlan(dni_client, sa_blob_client, account_id, cn_container_name, vl_blob_name, client_id, cn_id, reserv_id):
    """Create a topology VLAN."""
    print(f"Creating topology VLAN using {vl_blob_name}...")
    topo_id = create_topo(
        dni_client,
        sa_blob_client,
        account_id,
        cn_container_name,
        vl_blob_name,
        client_id,
        cn_id,
        reserv_id,
    )
    return topo_poll(dni_client, client_id, topo_id, polling_interval=30)


def delete_cloud_node(dni_client, client_id, topo_id, cn_id, reserv_id):
    """Delete a cloud node."""
    print(f"Deleting cloud node with ID {cn_id}...")
    dni_client.delete_resource(
        f"/accounts/{client_id}/resources/assets/vpns/cloud-nodes/{cn_id}"
    )
    dni_client.delete_resource(
        f"/accounts/{client_id}/resources/assets/vpns/topologies/{topo_id}"
    )
    dni_client.delete_resource(
        f"/accounts/{client_id}/resources/assets/vpns/locations/{reserv_id}"
    )


def main(method_name, **kwargs):
    """Main function to dynamically execute methods."""
    config_param = load_config()
    dni_client, sa_blob_client = initialize_clients(config_param)

    methods = {
        "get_staging_client": lambda: get_staging_client(
            dni_client, kwargs["account_id"], kwargs["client_name"]
        ),
        "get_bandwidth_reservation": lambda: get_bandwidth_reservation(
            dni_client, kwargs["account_id"], kwargs["service_provider_name"]
        ),
        "list_network_assets": lambda: list_network_assets(
            sa_blob_client, kwargs["container_name"]
        ),
        "create_cloud_node": lambda: create_cloud_node(
            dni_client,
            sa_blob_client,
            kwargs["account_id"],
            kwargs["cn_container_name"],
            kwargs["cn_blob_name"],
        ),
        "assign_location": lambda: assign_location(
            dni_client,
            sa_blob_client,
            kwargs["account_id"],
            kwargs["cn_container_name"],
            kwargs["loc_blob_name"],
            kwargs["client_id"],
            kwargs["cn_id"],
        ),
        "update_reachability": lambda: update_reachability(
            dni_client,
            sa_blob_client,
            kwargs["cn_container_name"],
            kwargs["reach_blob_name"],
            kwargs["client_id"],
            kwargs["cn_id"],
        ),
        "create_topology_vlan": lambda: create_topology_vlan(
            dni_client,
            sa_blob_client,
            kwargs["account_id"],
            kwargs["cn_container_name"],
            kwargs["vl_blob_name"],
            kwargs["client_id"],
            kwargs["cn_id"],
            kwargs["reserv_id"],
        ),
        "delete_cloud_node": lambda: delete_cloud_node(
            dni_client,
            kwargs["client_id"],
            kwargs["topo_id"],
            kwargs["cn_id"],
            kwargs["reserv_id"],
        ),
    }

    # Execute the selected method
    if method_name in methods:
        result = methods[method_name]()
        print("Execution result:", result)
    else:
        print(f"Invalid method name: {method_name}. Available methods: {list(methods.keys())}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--method", required=True, help="Name of the method to execute")
    parser.add_argument("--account_id", required=False)
    parser.add_argument("--client_name", required=False)
    parser.add_argument("--service_provider_name", required=False)
    parser.add_argument("--container_name", required=False)
    parser.add_argument("--cn_container_name", required=False)
    parser.add_argument("--cn_blob_name", required=False)
    parser.add_argument("--loc_blob_name", required=False)
    parser.add_argument("--reach_blob_name", required=False)
    parser.add_argument("--vl_blob_name", required=False)
    parser.add_argument("--client_id", required=False)
    parser.add_argument("--cn_id", required=False)
    parser.add_argument("--reserv_id", required=False)
    parser.add_argument("--topo_id", required=False)

    args = parser.parse_args()

    main(
        method_name=args.method,
        account_id=args.account_id,
        client_name=args.client_name,
        service_provider_name=args.service_provider_name,
        container_name=args.container_name,
        cn_container_name=args.cn_container_name,
        cn_blob_name=args.cn_blob_name,
        loc_blob_name=args.loc_blob_name,
        reach_blob_name=args.reach_blob_name,
        vl_blob_name=args.vl_blob_name,
        client_id=args.client_id,
        cn_id=args.cn_id,
        reserv_id=args.reserv_id,
        topo_id=args.topo_id,
    )
