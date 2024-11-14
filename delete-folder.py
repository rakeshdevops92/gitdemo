import os
import logging
import json
import azure.functions as func
from azure.storage.blob import BlobServiceClient
from azure.identity import ManagedIdentityCredential

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function to delete folder contents processed a request.')
    try:
        folder_path = req.params.get('folder')
        if not folder_path:
            try:
                req_body = req.get_json()
            except ValueError:
                pass
            else:
                folder_path = req_body.get('folder')
        
        if folder_path:
            resp = ""
            azure_container_name = 'a360root'
            service = BlobServiceClient(
                os.environ.get("BLOB_STORAGE_ACCOUNT_URL"), 
                credential=ManagedIdentityCredential()
            )
            container_client = service.get_container_client(azure_container_name)
            
            blobs_to_delete = container_client.list_blobs(name_starts_with=folder_path)

            deleted_blobs = []
            for blob in blobs_to_delete:
                blob_client = container_client.get_blob_client(blob.name)
                blob_client.delete_blob()
                deleted_blobs.append(blob.name)
            
            if deleted_blobs:
                resp = {
                    "status": "success",
                    "deleted_blobs": deleted_blobs
                }
            else:
                resp = {
                    "status": "fail",
                    "errdesc": "No blobs found in the specified folder or folder does not exist"
                }
            return func.HttpResponse(json.dumps(resp), status_code=200, mimetype='application/json')

        else:
            return func.HttpResponse(
                "You need to pass the name of the folder to be deleted",
                status_code=200
            )

    except Exception as e:
        logging.error(f"Error deleting folder contents: {str(e)}")
        return func.HttpResponse(
            json.dumps({"status": "error", "errdesc": str(e)}),
            status_code=500,
            mimetype='application/json'
        )
