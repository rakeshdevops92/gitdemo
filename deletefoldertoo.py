from azure.storage.blob import BlobServiceClient, ContainerClient, BlobClient
import os
import logging
import json
from azure.identity import ManagedIdentityCredential

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.basicConfig(level=logging.DEBUG)  # Set log level to DEBUG for verbose logging
    logging.info("Azure HTTP trigger function to delete folder contents started.")

    try:
        # Extract the folder path from the request
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
                status_code=400,
            )

        logging.info(f"Received request to delete folder: {path}")

        # Initialize Blob Service Client
        azure_container_name = 'a360root'
        blob_service_client = BlobServiceClient(
            os.environ.get("BLOB_STORAGE_ACCOUNT_URL"),
            credential=ManagedIdentityCredential()
        )
        container_client = blob_service_client.get_container_client(azure_container_name)

        # List all blobs in the specified folder
        blob_list = container_client.list_blobs(name_starts_with=path)
        blobs_to_delete = []
        deleted_files_count = 0

        logging.debug(f"Listing blobs under the folder: {path}")
        for blob in blob_list:
            blobs_to_delete.append(blob.name)
            logging.debug(f"Identified blob for deletion: {blob.name}")

        if not blobs_to_delete:
            logging.info(f"No blobs found under the folder: {path}")
            return func.HttpResponse(
                json.dumps({"status": "success", "message": "No files to delete."}),
                status_code=200,
                mimetype="application/json",
            )

        # Delete all blobs
        logging.info(f"Starting deletion of {len(blobs_to_delete)} blobs.")
        for blob_name in blobs_to_delete:
            try:
                blob_client = container_client.get_blob_client(blob_name)
                blob_client.delete_blob()
                deleted_files_count += 1
                logging.debug(f"Successfully deleted blob: {blob_name}")
            except Exception as e:
                logging.error(f"Failed to delete blob: {blob_name}. Error: {e}")

        logging.info(f"Total files successfully deleted: {deleted_files_count}")

        # Delete the folder (only for hierarchical namespace storage or logical placeholder blobs)
        try:
            logging.info(f"Attempting to delete the folder (prefix): {path}")
            container_client.delete_blob(path)
            logging.info(f"Successfully deleted the folder: {path}")
        except Exception as e:
            logging.warning(f"Failed to delete folder (prefix): {path}. Error: {e}")

        response = {
            "status": "success",
            "deleted_files_count": deleted_files_count,
            "message": f"All files and folder '{path}' have been processed.",
        }
        logging.debug(f"Response: {response}")
        return func.HttpResponse(
            json.dumps(response),
            status_code=200,
            mimetype="application/json",
        )

    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        logging.error(error_message, exc_info=True)
        return func.HttpResponse(
            json.dumps({"status": "fail", "error": str(e)}),
            status_code=500,
            mimetype="application/json",
        )
