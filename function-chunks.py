import os
import logging
from azure.identity.aio import ManagedIdentityCredential
from azure.storage.blob.aio import BlobServiceClient
from datetime import datetime
import ibm_boto3
from ibm_botocore.client import Config

DEFAULT_CHUNK_SIZE = 2 * 1024 * 1024 * 1024  # 2 GB

def download_chunk(bucket_name, key, start_byte, end_byte, part_number, temp_file_path, cos_client):
    range_header = f'bytes={start_byte}-{end_byte}'
    temp_file_chunk_path = f"{temp_file_path}.part{part_number}"

    response = cos_client.get_object(Bucket=bucket_name, Key=key, Range=range_header)
    with open(temp_file_chunk_path, 'wb') as f:
        f.write(response['Body'].read())

    logging.info(f'Chunk {part_number} downloaded: {start_byte} to {end_byte}')
    return temp_file_chunk_path

def merge_chunks(temp_file_path, local_file_path, num_parts):
    with open(local_file_path, 'wb') as output_file:
        for part_number in range(1, num_parts + 1):
            temp_file_chunk_path = f"{temp_file_path}.part{part_number}"
            with open(temp_file_chunk_path, 'rb') as chunk_file:
                output_file.write(chunk_file.read())
            os.remove(temp_file_chunk_path)  # Remove the chunk file after merging

    logging.info(f"All chunks merged into {local_file_path}")

async def main(req: func.HttpRequest) -> func.HttpResponse:
    blob_name = ""
    timeStartPost = ""
    timeEndPost = ""
    fileByteArray = None
    try:
        # Hardcoded credentials from your screenshot
        COS_ENDPOINT = "https://s3.us-south.cloud-object-storage.appdomain.cloud"
        COS_API_KEY_ID = "s2oSRxynX2SygYAgj408ZwaroiW7o_8QqJzEYvfV57kuj"
        COS_INSTANCE_CRN = "crn:v1:bluemix:public:cloud-object-storage:global:a/d597f2a311fa4de2b7679fe807c74b08:1a41e1ad-a035-4cc6-8032-XXXX::"

        proxy = "http://vz-proxy.pncint.net:80"
        os.environ["https_proxy"] = proxy

        cos_client = ibm_boto3.client("s3",
                                      ibm_api_key_id=COS_API_KEY_ID,
                                      ibm_service_instance_id=COS_INSTANCE_CRN,
                                      config=Config(signature_version="oauth"),
                                      endpoint_url=COS_ENDPOINT)

        bucket_name = req.params.get('bucket_name')
        blob_name = req.params.get('blob_name')
        key = req.params.get('key')

        if not all([blob_name, bucket_name, key]):
            return func.HttpResponse("Missing parameters", status_code=400)

        chunk_size = DEFAULT_CHUNK_SIZE

        temp_file_path = f"/tmp/{blob_name}"

        response = cos_client.head_object(Bucket=bucket_name, Key=key)
        file_size = response['ContentLength']
        num_parts = file_size // chunk_size + (1 if file_size % chunk_size > 0 else 0)

        for part_number in range(1, num_parts + 1):
            start_byte = (part_number - 1) * chunk_size
            end_byte = min(start_byte + chunk_size - 1, file_size - 1)
            download_chunk(bucket_name, key, start_byte, end_byte, part_number, temp_file_path, cos_client)

        local_file_path = f"/tmp/{blob_name}_merged"
        merge_chunks(temp_file_path, local_file_path, num_parts)

        global blobServiceClient, containerClient
        if blobServiceClient is None:
            blobServiceClient = BlobServiceClient(os.environ.get("BLOB_STORAGE_ACCOUNT_URL"), credential=ManagedIdentityCredential())
        if containerClient is None:
            containerClient = blobServiceClient.get_container_client(os.environ.get("BLOB_STORAGE_CONTAINER_NAME"))

        async with containerClient:
            async with open(local_file_path, "rb") as data:
                await containerClient.upload_blob(name=blob_name, data=data, overwrite=True)

        logging.info(f"Uploaded {blob_name} to Azure Blob Storage")

        return func.HttpResponse(json.dumps({"status": "success", "blob_name": blob_name}), status_code=200, mimetype="application/json")
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return func.HttpResponse(json.dumps({"status": "fail", "error": str(e)}), status_code=500, mimetype="application/json")
