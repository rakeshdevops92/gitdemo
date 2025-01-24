import argparse

def main(method_name, **kwargs):
    methods = {
        "create_cloud_node": create_cloud_node,
        "assign_location": assign_location,
        "update_reachability": update_reachability,
    }

    if method_name in methods:
        methods[method_name](**kwargs)
    else:
        print(f"Invalid method name: {method_name}. Available methods: {list(methods.keys())}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--method", required=True, help="Name of the method to execute")
    parser.add_argument("--cn_container_name", required=False)
    parser.add_argument("--cn_blob_name", required=False)
    parser.add_argument("--loc_blob_name", required=False)
    parser.add_argument("--reach_blob_name", required=False)
    parser.add_argument("--account_id", required=False)
    parser.add_argument("--client_id", required=False)
    parser.add_argument("--cn_id", required=False)
    parser.add_argument("--reserv_id", required=False)

    args = parser.parse_args()

    main(
        args.method,
        dni_client=None,
        sa_blob_client=None,
        account_id=args.account_id,
        cn_container_name=args.cn_container_name,
        cn_blob_name=args.cn_blob_name,
        loc_blob_name=args.loc_blob_name,
        reach_blob_name=args.reach_blob_name,
        client_id=args.client_id,
        cn_id=args.cn_id,
        reserv_id=args.reserv_id,
    )
