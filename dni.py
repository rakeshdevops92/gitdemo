import argparse
import json
import os
from azure_storage_blob import BlobServiceClient
from dni_client_helper import (
    DNIClient,
    SaBlobClient,
    create_cn,
    assign_loc,
    update_reach,
    create_topo,
    topo_poll,
)

def load_config():
    with open("access.json", "r") as config_file:
        return json.load(config_file)

def initialize_clients():
    tenant_id = os.getenv("tenant_id")
    app_id = os.getenv("app_id")
    passwd = os.getenv("passwd")
    account_id = os.getenv("account_id")
    rm_url = os.getenv("rm_url")
    sa_connect_str = os.getenv("sa_connect_str")

    dni_client = DNIClient(
        base_url=rm_url,
        client_id=app_id,
        client_secret=passwd,
        tenant_id=tenant_id,
        scope="api://df62135d-2ede-4bac-9465-a36750479690/.default",
    )
    sa_blob_client = SaBlobClient(sa_connect_str=sa_connect_str)
    return dni_client, sa_blob_client, account_id

def get_staging_client(dni_client, account_id, client_name):
    clients = dni_client.get_resources(f"/accounts/{account_id}/resources/clients")[
        "result"
    ]
    stg_client = next(client for client in clients if client["name"] == client_name)
    return stg_client["id"]

def create_cloud_node(dni_client, sa_blob_client, account_id, cn_container_name, cn_blob_name):
    return create_cn(dni_client, sa_blob_client, account_id, cn_container_name, cn_blob_name)

def assign_location(dni_client, sa_blob_client, account_id, cn_container_name, loc_blob_name, client_id, cn_id):
    return assign_loc(dni_client, sa_blob_client, account_id, cn_container_name, loc_blob_name, client_id, cn_id)

def update_reachability(dni_client, sa_blob_client, cn_container_name, reach_blob_name, client_id, cn_id):
    return update_reach(dni_client, sa_blob_client, cn_container_name, reach_blob_name, client_id, cn_id)

def create_topology_vlan(dni_client, sa_blob_client, account_id, cn_container_name, vl_blob_name, client_id, cn_id, reserv_id):
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
    dni_client.delete_resource(
        f"/accounts/{client_id}/resources/assets/vpns/cloud-nodes/{cn_id}"
    )
    dni_client.delete_resource(
        f"/accounts/{client_id}/resources/assets/vpns/topologies/{topo_id}"
    )
    dni_client.delete_resource(
        f"/accounts/{client_id}/resources/assets/vpns/locations/{reserv_id}"
    )

def main(method_name):
    dni_client, sa_blob_client, account_id = initialize_clients()

    context = {}

    methods = {
        "get_staging_client": lambda: context.update(
            client_id=get_staging_client(
                dni_client, account_id, "default-client-name"
            )
        ),
        "create_cloud_node": lambda: context.update(
            cn_id=create_cloud_node(
                dni_client,
                sa_blob_client,
                account_id,
                "cloudnode-container",
                "cloudnode.json",
            )
        ),
        "assign_location": lambda: context.update(
            reserv_id=assign_location(
                dni_client,
                sa_blob_client,
                account_id,
                "cloudnode-container",
                "location.json",
                context.get("client_id"),
                context.get("cn_id"),
            )
        ),
        "update_reachability": lambda: update_reachability(
            dni_client,
            sa_blob_client,
            "cloudnode-container",
            "reachability.json",
            context.get("client_id"),
            context.get("cn_id"),
        ),
        "create_topology_vlan": lambda: context.update(
            topo_id=create_topology_vlan(
                dni_client,
                sa_blob_client,
                account_id,
                "cloudnode-container",
                "vlan.json",
                context.get("client_id"),
                context.get("cn_id"),
                context.get("reserv_id"),
            )
        ),
        "delete_cloud_node": lambda: delete_cloud_node(
            dni_client,
            context.get("client_id"),
            context.get("topo_id"),
            context.get("cn_id"),
            context.get("reserv_id"),
        ),
    }

    if method_name in methods:
        methods[method_name]()
    else:
        print(f"Invalid method name: {method_name}. Available methods: {list(methods.keys())}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--method", required=True, help="Name of the method to execute")
    args = parser.parse_args()
    main(method_name=args.method)
