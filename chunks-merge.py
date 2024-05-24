import os
import ibm_boto3
from ibm_botocore.client import Config, ClientError
from pathlib import Path
import time
from datetime import datetime
import sys

# Constants for IBM COS values
COS_ENDPOINT = "https://s3.us-south.cloud-object-storage.appdomain.cloud"
COS_API_KEY_ID = "s2oSRxqnxZsgYqj408Zwaro1w70_8QqjZEVfv57kuj"
COS_INSTANCE_CRN = "crn:v1:bluemix:public:cloud-object-storage:global:a/d597f2a311fa4de2b7679fe807c74b08:1a41e1ad-a035-4cc6-8032-e57a5132bd3a::"
proxy = "http://vz-proxy.pncint.net:80"
os.environ["https_proxy"] = proxy

# Create resource
cos = ibm_boto3.resource(
    "s3",
    ibm_api_key_id=COS_API_KEY_ID,
    ibm_service_instance_id=COS_INSTANCE_CRN,
    config=Config(signature_version="oauth"),
    endpoint_url=COS_ENDPOINT
)

def download_chunk(bucket_name, key, start_byte, end_byte, part_number, temp_file_path):
    range_header = f'bytes={start_byte}-{end_byte}'
    response = cos.meta.client.get_object(Bucket=bucket_name, Key=key, Range=range_header)
    temp_file_chunk_path = f"{temp_file_path}.part{part_number}"
    with open(temp_file_chunk_path, 'wb') as f:
        f.write(response['Body'].read())
    print(f'Chunk {part_number} downloaded: {start_byte} to {end_byte}')

def merge_chunks(temp_file_path, local_file_path, num_parts):
    with open(local_file_path, 'wb') as output_file:
        for part_number in range(1, num_parts + 1):
            temp_file_chunk_path = f"{temp_file_path}.part{part_number}"
            with open(temp_file_chunk_path, 'rb') as chunk_file:
                output_file.write(chunk_file.read())
            os.remove(temp_file_chunk_path)  # Remove the chunk file after merging
    print(f"All chunks merged into {local_file_path}")

def download_bucket_contents(bucket_name):
    print("Retrieving bucket contents from: {0}".format(bucket_name))
    try:
        files = cos.Bucket(bucket_name).objects.all()
        for file in files:
            print("********************************************************")
            start = time.time()
            Start_time = datetime.now()
            print("Item Start Time = ", Start_time)
            print("Downloading Item: {0} ({1} bytes)".format(file.key, file.size))

            local_path_filename = "/home/pj72963/IDF_PY/" + file.key
            directory_path = os.path.dirname(local_path_filename)
            Path(directory_path).mkdir(parents=True, exist_ok=True)
            temp_file_path = local_path_filename + ".temp"

            if file.size > 0:
                part_size = 2 * 1024 * 1024 * 1024  # 2GB
                part_number = 1
                num_parts = (file.size + part_size - 1) // part_size
                for start_byte in range(0, file.size, part_size):
                    end_byte = min(start_byte + part_size - 1, file.size - 1)
                    download_chunk(bucket_name, file.key, start_byte, end_byte, part_number, temp_file_path)
                    part_number += 1
                merge_chunks(temp_file_path, local_path_filename, num_parts)
                print("Successfully Downloaded and Merged")
            else:
                print("Skipping Item because Item size is Zero byte")

            end = time.time()
            Time_elapsed = end - start
            print("Item Time_elapsed = ", Time_elapsed)
            end_time = datetime.now()
            print("Item End Time = ", end_time)

    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to retrieve bucket contents: {0}".format(e))
