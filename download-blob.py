from datetime import datetime
import os
import logging
import traceback
import json
import azure.functions as func
from azure.storage.blob.aio import BlobServiceClient
from azure.identity.aio import ManagedIdentityCredential
import re

blobServiceClient = None

def get_file_name(path):
    last_index_of_slash = path.rindex("/")
    if last_index_of_slash == -1:
        return path
    return path[last_index_of_slash + 1:]

async def main(req: func.HttpRequest) -> func.HttpResponse:
    global blobServiceClient
    try:
        path = req.params.get('name')
        action = req.params.get('action')  # Check if action parameter is provided for listing blobs

        if not path and not action:
            try:
                req_body = req.get_json()
            except ValueError:
                pass
            else:
                path = req_body.get('name')
                action = req_body.get('action')

        container = os.environ.get("BLOB_STORAGE_CONTAINER_NAME_OIMS")
        if blobServiceClient is None:
            blobServiceClient = BlobServiceClient(
                os.environ.get("BLOB_STORAGE_ACCOUNT_URL"), credential=ManagedIdentityCredential()
            )

        if action == 'list':
            container_client = blobServiceClient.get_container_client(container)
            blob_list = container_client.list_blobs()

            files = []
            async for blob in blob_list:
                files.append({
                    "file_name": blob.name,
                    "size_in_bytes": blob.size,
                    "last_modified": str(blob.last_modified)
                })

            return func.HttpResponse(
                json.dumps({"status": "success", "files": files}),
                status_code=200,
                mimetype='application/json'
            )

        if path:
            timeStartGet = datetime.utcnow().isoformat(sep=" ", timespec="milliseconds")
            logging.info("Start Get File " + path + " " + timeStartGet)

            blobClient = blobServiceClient.get_blob_client(container=container, blob=path)
            if await blobClient.exists() == False:
                oldBlobPath = re.sub('^(.*)(?=usr)', "", path)
                tarFileWithoutRetention = (path.split("/")[0]).strip()
                blobClient = blobServiceClient.get_blob_client(container=container, blob=(tarFileWithoutRetention + "_5" + "/" + oldBlobPath))

            if await blobClient.exists() == False:
                blobClient = blobServiceClient.get_blob_client(container=container, blob=(tarFileWithoutRetention + "_7" + "/" + oldBlobPath))
            if await blobClient.exists() == False:
                blobClient = blobServiceClient.get_blob_client(container=container, blob=(tarFileWithoutRetention + "_3" + "/" + oldBlobPath))
            if await blobClient.exists() == False:
                blobClient = blobServiceClient.get_blob_client(container=container, blob=(tarFileWithoutRetention + "_1" + "/" + oldBlobPath))
            if await blobClient.exists() == False:
                blobClient = blobServiceClient.get_blob_client(container=container, blob=(tarFileWithoutRetention + "_10" + "/" + oldBlobPath))
            if await blobClient.exists() == False:
                blobClient = blobServiceClient.get_blob_client(container=container, blob=(tarFileWithoutRetention + "_15" + "/" + oldBlobPath))
            if await blobClient.exists() == False:
                blobClient = blobServiceClient.get_blob_client(container=container, blob=oldBlobPath)

            if await blobClient.exists():
                downloader = await blobClient.download_blob()
                prop = await blobClient.get_blob_properties()
                encryptkeyversion = ""
                if prop.metadata.get("encryptkeyversion"):
                    encryptkeyversion = prop.metadata.get("encryptkeyversion")
                timeEndGet = datetime.utcnow().isoformat(sep=" ", timespec="milliseconds")
                logging.info("End Get File " + path + " " + timeEndGet)

                headers = {
                    "encryptkeyversion": encryptkeyversion,
                    "Content-Type": "application/octet-stream",
                    "Content-disposition": f"attachment; filename={get_file_name(path)}",
                    "Logs": "File " + path + " " + timeStartGet + " " + timeEndGet
                }
                return func.HttpResponse(await downloader.content_as_bytes(), headers=headers, status_code=200)
            else:
                timeFileNotFound = datetime.utcnow().isoformat(sep=" ", timespec="milliseconds")
                headers = {"Logs": "File " + path + " " + timeFileNotFound + " AzureFileNotFound "}
                return func.HttpResponse(json.dumps({"status": "fail", "errdesc": "File Not Found"}), headers=headers, status_code=404)

        return func.HttpResponse(
            json.dumps({"status": "fail", "message": "Please specify a valid action or file name."}),
            status_code=400,
            mimetype='application/json'
        )

    except Exception as e:
        logging.info('Error :' + traceback.format_exc())
        return func.HttpResponse(json.dumps({"status": "fail", "errdesc": traceback.format_exc()}), status_code=500, mimetype='application/json')
