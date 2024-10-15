import os
from azure.storage.blob.aio import BlobServiceClient
from azure.identity.aio import ManagedIdentityCredential

async def upload_file_activity(file_info: dict):
    try:
        blob_name = file_info['blob_name']
        file_byte_array = file_info['file_byte_array']
        storage_account_url = os.environ.get('BLOB_STORAGE_ACCOUNT_URL')
        container_name = os.environ.get('BLOB_STORAGE_CONTAINER_NAME_OIMS')

        blob_service_client = BlobServiceClient(account_url=storage_account_url, credential=ManagedIdentityCredential())
        container_client = blob_service_client.get_container_client(container_name)

        await container_client.upload_blob(name=blob_name, data=file_byte_array, overwrite=True)
        return {"status": "success", "blob": blob_name}

    except Exception as e:
        return {"status": "fail", "error": str(e)}
