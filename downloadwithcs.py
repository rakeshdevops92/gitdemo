import os
from azure.storage.blob import BlobServiceClient
from logging import INFO, getLogger
from azure.monitor.opentelemetry import configure_azure_monitor
from datetime import datetime

configure_azure_monitor()
logger = getLogger(__name__)
logger.setLevel(INFO)

def main(input: dict) -> dict:
    logger.info(f"Received request data: {input}")

    try:
        file_name = input.get("filepath")
        if not file_name:
            logger.error("Filepath not provided for download action")
            return {"status": "fail", "message": "Filepath not provided"}

        connection_string = "AZURE_STORAGE_CONNECTION_STRING"
        if not connection_string:
            logger.error("Storage connection string not found in environment variables")
            return {"status": "fail", "message": "Connection string not found"}

        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        container_name = os.getenv("BLOB_STORAGE_CONTAINER_NAME")
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)

        if not blob_client.exists():
            logger.error("Specified file not found in Azure storage")
            return {"status": "fail", "message": "File not found in Azure storage"}

        local_path = f"/tmp/{file_name}"

        logger.info(f"Downloading {file_name} to local path: {local_path}")
        with open(local_path, "wb") as download_file:
            download_stream = blob_client.download_blob()
            download_file.write(download_stream.readall())

        logger.info(f"File '{file_name}' downloaded successfully to '{local_path}'")
        return {"status": "success", "message": f"File downloaded to {local_path}"}

    except Exception as e:
        logger.error(f"Error in BlobDownloadActivity: {str(e)}")
        return {"status": "fail", "message": str(e)}
