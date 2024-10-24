import os
import re
from azure.storage.blob.aio import BlobServiceClient
from azure.identity.aio import ManagedIdentityCredential
from datetime import datetime

async def main(request_data: dict) -> dict:
    try:
        file_name = request_data.get('name')
        if not file_name:
            return {
                "status": "fail",
                "message": "No file name provided"
            }
        container_name = os.environ.get("BLOB_STORAGE_CONTAINER_NAME_OIMS")
        blob_service_client = BlobServiceClient(
            os.environ.get("BLOB_STORAGE_ACCOUNT_URL"), 
            credential=ManagedIdentityCredential()
        )
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)

        if not await blob_client.exists():
            return {
                "status": "fail",
                "message": "File not found"
            }
        downloader = await blob_client.download_blob()
        file_content = await downloader.content_as_bytes()

        return {
            "status": "success",
            "file_content": file_content.decode('utf-8')
        }
    
    except Exception as e:
        return {
            "status": "fail",
            "message": str(e)
        }
