
import logging
from azure.storage.blob.aio import BlobServiceClient
from datetime import datetime
from opentelemetry import trace
from opentelemetry.instrumentation.logging import LoggingInstrumentor

LoggingInstrumentor().instrument(set_logging_format=True)
tracer = trace.get_tracer(__name__)

async def main(blobdata: dict):
    blob_name = blobdata['blob_name']
    filepath = blobdata['filepath']

    with tracer.start_as_current_span("durable_function_activity"):
        with open(filepath, "rb") as file:
            fileByteArray = file.read()

        connection_string = "your_connection_string_here"
        blobServiceClient = BlobServiceClient.from_connection_string(connection_string)

        container_name = "oimreports"
        containerClient = blobServiceClient.get_container_client(container_name)

        await containerClient.upload_blob(name=blob_name, data=fileByteArray, overwrite=True)

        timeEndPost = datetime.utcnow().isoformat(sep=" ", timespec="milliseconds")
        logging.info(f"End Post File {blob_name} from {filepath} at {timeEndPost}")

        return {"status": "success", "file": blob_name, "timeEndPost": timeEndPost}
