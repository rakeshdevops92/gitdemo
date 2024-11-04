import os
from azure.storage.blob import BlobServiceClient
from logging import INFO, getLogger
from azure.monitor.opentelemetry import configure_azure_monitor

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

        container_name = os.getenv("BLOB_STORAGE_CONTAINER_NAME")
        connection_string = "BLOB_STORAGE_CONNECTION_STRING"

        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)

        logger.info(f"Blob Client Details - Container: {blob_client.container_name}, Blob: {blob_client.blob_name}, URL: {blob_client.url}")

        logger.info("Detailed blob_client attributes:")
        for attribute in dir(blob_client):
            if not attribute.startswith("_"):  # Skip private attributes
                try:
                    value = getattr(blob_client, attribute)
                    logger.info(f"{attribute}: {value}")
                except Exception as e:
                    logger.warning(f"Could not access attribute {attribute}: {e}")
                    
        if not blob_client.exists():
            logger.error("Specified file not found in Azure storage")
            return {"status": "fail", "message": "File not found in Azure storage"}

        local_path = os.path.join(os.getcwd(), os.path.basename(file_name))
        logger.info(f"Downloading {file_name} to local path: {local_path}")

        with open(local_path, "wb") as download_file:
            download_stream = blob_client.download_blob()
            download_file.write(download_stream.readall())

        logger.info(f"File '{file_name}' downloaded successfully to '{local_path}'")
        return {"status": "success", "message": f"File downloaded to {local_path}"}
    
    except Exception as e:
        logger.error(f"Error in BlobDownloadActivity: {str(e)}")
        return {"status": "fail", "message": str(e)}
