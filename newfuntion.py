import os
from azure.storage.blob import BlobServiceClient
from datetime import datetime
import paramiko
import logging
import io

blobServiceClient = None
containerClient = None

SSH_HOST = os.environ.get("SSH_HOST")
SSH_PORT = int(os.environ.get("SSH_PORT", 22))
SSH_USERNAME = os.environ.get("SSH_USERNAME")
SSH_PASSWORD = os.environ.get("SSH_PASSWORD")
BLOB_STORAGE_CONNECTION_STRING = os.environ.get("BLOB_STORAGE_CONNECTION_STRING")
STORAGE_ACCOUNT_NAME = "staarkaze2022"
CONTAINER_NAME = "oimreports"
SSH_SOURCE_PATH = "/ark/landing_zone/oim_reports"

async def main(req) -> func.HttpResponse:
    global blobServiceClient, containerClient
    timeStartPost = ""
    timeEndPost = ""
    try:
        ssh_client = connect_to_ssh(SSH_HOST, SSH_PORT, SSH_USERNAME, SSH_PASSWORD)
        sftp_files = list_files_via_ssh(ssh_client, SSH_SOURCE_PATH)
        
        for filename in sftp_files:
            file_content = download_file_via_ssh(ssh_client, SSH_SOURCE_PATH, filename)
            blob_name = filename

            if blobServiceClient is None:
                blobServiceClient = BlobServiceClient.from_connection_string(BLOB_STORAGE_CONNECTION_STRING)
                
            if containerClient is None:
                containerClient = blobServiceClient.get_container_client(CONTAINER_NAME)

            timeStartPost = datetime.utcnow().isoformat(sep=" ", timespec="milliseconds")
            logging.info(f"Start Post File: {blob_name} at {timeStartPost}")
            
            metadata = {"source": SSH_HOST, "encryptkeyversion": req.headers.get("encryptkeyversion")}
            containerClient.upload_blob(name=blob_name, data=file_content, metadata=metadata, overwrite=True)

            timeEndPost = datetime.utcnow().isoformat(sep=" ", timespec="milliseconds")
            logging.info(f"End Post File: {blob_name} at {timeEndPost}")

        ssh_client.close()

        resp = {
            "status": "success",
            "files_uploaded": sftp_files,
            "timeEndPost": timeEndPost,
            "timeStartPost": timeStartPost,
            "errdesc": ""
        }
        return func.HttpResponse(json.dumps(resp), status_code=200, mimetype='application/json')

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        resp = {"status": "fail", "errdesc": str(e)}
        return func.HttpResponse(json.dumps(resp), status_code=500, mimetype='application/json')

def connect_to_ssh(host, port, username, password):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=host, port=port, username=username, password=password)
    return ssh_client

def list_files_via_ssh(ssh_client, source_path):
    stdin, stdout, stderr = ssh_client.exec_command(f"ls -1 {source_path}")
    files = stdout.read().decode().splitlines()
    logging.info(f"Files found via SSH: {files}")
    return files

def download_file_via_ssh(ssh_client, source_path, filename):
    sftp = ssh_client.open_sftp()
    file_path = os.path.join(source_path, filename)
    with sftp.open(file_path, "rb") as file:
        file_content = file.read()
    return io.BytesIO(file_content)
