import os
import logging
import json
import azure.functions as func
from azure.storage.blob import BlobServiceClient
from azure.identity import ManagedIdentityCredential

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.basicConfig(level=logging.INFO)  # Set the log level to INFO
    logging.info("Azure HTTP trigger function to delete folder contents started.")

    try:
        path = req.params.get('name')
        if not path:
            try:
                req_body = req.get_json()
                path = req_body.get('name')
            except ValueError:
                pass

        if not path:
            logging.error("No 'name' parameter provided in the request.")
            return func.HttpResponse(
                "You need to pass the name of the folder to be deleted.",
                status_code=400
            )

        logging.info(f"Received request to delete contents of folder: {path}")

        azure_container_name = 'a360root'
        blob_service_client = BlobServiceClient(
            os.environ.get("BLOB_STORAGE_ACCOUNT_URL"),
            credential=ManagedIdentityCredential()
        )
        
        container_client = blob_service_client.get_container_client(azure_container_name)
        blob_list = container_client.list_blobs(name_starts_with=path)
        
        deleted_files_count = 0
        blobs_to_delete = []

        for blob in blob_list:
            blobs_to_delete.append(blob.name)
            logging.info(f"Identified blob for deletion: {blob.name}")

        if not blobs_to_delete:
            logging.info(f"No blobs found under the folder: {path}")
            return func.HttpResponse(
                json.dumps({"status": "success", "message": "No files to delete."}),
                status_code=200,
                mimetype="application/json"
            )

        logging.info(f"Total files identified for deletion: {len(blobs_to_delete)}")
        
        for blob_name in blobs_to_delete:
            try:
                blob_client = container_client.get_blob_client(blob_name)
                blob_client.delete_blob()
                deleted_files_count += 1
                logging.info(f"Successfully deleted blob: {blob_name}")
            except Exception as e:
                logging.error(f"Failed to delete blob: {blob_name}. Error: {e}")

        logging.info(f"Total files successfully deleted: {deleted_files_count}")

        response = {
            "status": "success",
            "deleted_files_count": deleted_files_count,
            "message": f"All files in the folder '{path}' have been processed."
        }
        
        return func.HttpResponse(
            json.dumps(response),
            status_code=200,
            mimetype="application/json"
        )
        
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return func.HttpResponse(
            json.dumps({"status": "fail", "error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )
