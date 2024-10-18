import logging
from azure.storage.blob.aio import BlobServiceClient
from datetime import datetime

async def main(blobdata: dict):
    try:
        blob_name = blobdata['blob_name']
        filepath = blobdata['filepath']
        
        with open(filepath, "rb") as file:
            fileByteArray = file.read()

        connection_string = "connection-string"
        blobServiceClient = BlobServiceClient.from_connection_string(connection_string)

        container_name = "test"
        containerClient = blobServiceClient.get_container_client(container_name)

        await containerClient.upload_blob(name=blob_name, data=fileByteArray, overwrite=True)

        timeEndPost = datetime.utcnow().isoformat(sep=".", timespec="milliseconds")
        logging.info(f"End Post File {blob_name} from {filepath} at {timeEndPost}")

        return {"status": "success", "file": blob_name, "timeEndPost": timeEndPost}

    except Exception as ex:
        logging.error(f"Error: {str(ex)}")
        return {"status": "fail", "errdesc": str(ex)}
