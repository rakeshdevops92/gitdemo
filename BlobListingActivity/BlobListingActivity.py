import os
import json
from azure.storage.blob import BlobServiceClient
from azure.identity import ManagedIdentityCredential

async def main(request_data: dict) -> dict:
    try:
        container_name = os.environ.get("BLOB_STORAGE_CONTAINER_NAME_OIMS")
        blob_service_client = BlobServiceClient(
            os.environ.get("BLOB_STORAGE_ACCOUNT_URL"), 
            credential=ManagedIdentityCredential()
        )

        container_client = blob_service_client.get_container_client(container_name)
        blob_list = container_client.list_blobs()

        files = []
        for blob in blob_list:
            files.append({
                "file_name": blob.name,
                "size_in_bytes": blob.size,
                "last_modified": str(blob.last_modified)
            })

        return {
            "status": "success",
            "files": files
        }
    
    except Exception as e:
        return {
            "status": "fail",
            "message": str(e)
        }
