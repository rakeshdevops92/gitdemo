from azure.storage.blob.aio import BlobServiceClient
import logging
from datetime import datetime

blobServiceClient = None
containerClient = None

async def main(context):
    input_data = context.get_input()
    blob_name = input_data["blob_name"]
    fileByteArray = input_data["fileByteArray"]

    try:
        global blobServiceClient, containerClient
        if blobServiceClient is None:
            logging.info(f"New Connection GET BlobServiceClient for {blob_name}")
            connection_string = "DefaultEndpointsProtocol=https;AccountName=staarkaze2022;AccountKey=5VcxQ+irR32bVG9J+ZGawFYXyNrxt0s21NelyuDpbmbbXdArfAdkbKHJvNQS;EndpointSuffix=core.windows.net"
            blobServiceClient = BlobServiceClient.from_connection_string(connection_string)

        if containerClient is None:
            logging.info(f"New Connection GET ContainerClient for {blob_name}")
            container_name = os.getenv("BLOB_STORAGE_CONTAINER_NAME_OIMS")
            containerClient = blobServiceClient.get_container_client(container_name)

        await containerClient.upload_blob(name=blob_name, data=fileByteArray, overwrite=True)

        timeEndPost = datetime.utcnow().isoformat(sep="-", timespec="milliseconds")
        logging.info(f"End Post File {blob_name} at {timeEndPost}")

        return {"status": "success", "file": blob_name, "timeEndPost": timeEndPost}

    except Exception as ex:
        logging.error(f"Activity exception: {str(ex)}")
        return {"status": "fail", "error": str(ex)}
