from azure.storage.blob.aio import BlobServiceClient
from datetime import datetime
from logging import INFO, getLogger
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor()
logger = getLogger(__name__)
logger.setLevel(INFO)

async def main(blobdata: dict):
    blob_name = blobdata['blob_name']
    filepath = blobdata['filepath']

    try:
        with open(filepath, "rb") as file:
            fileByteArray = file.read()

        connection_string = "your_connection_string_here"
        blobServiceClient = BlobServiceClient.from_connection_string(connection_string)

        container_name = "oimreports"
        containerClient = blobServiceClient.get_container_client(container_name)

        await containerClient.upload_blob(name=blob_name, data=fileByteArray, overwrite=True)

        timeEndPost = datetime.utcnow().isoformat(sep=" ", timespec="milliseconds")
        logger.info(f"End Post File {blob_name} from {filepath} at {timeEndPost}")

        return {"status": "success", "file": blob_name, "timeEndPost": timeEndPost}
    
    except Exception as ex:
        logger.error(f"Error: {str(ex)}")
        return {"status": "fail", "errdesc": str(ex)}
