import os

# Define the folder structure and files
folders_and_files = {
    "orchestrator_function": {
        "__init__.py": """import azure.functions as func
import azure.durable_functions as df

def orchestrator_function(context: df.DurableOrchestrationContext):
    request_data = context.get_input()
    
    action = request_data.get('action')
    if action == 'list':
        # Call the blob listing activity
        result = yield context.call_activity('BlobListingActivity', request_data)
    else:
        # Call the file downloading activity
        result = yield context.call_activity('BlobDownloadActivity', request_data)
    
    return result

main = df.Orchestrator.create(orchestrator_function)
""",
        "function.json": """{
  "bindings": [
    {
      "name": "context",
      "type": "orchestrationTrigger",
      "direction": "in"
    }
  ]
}
"""
    },
    "BlobListingActivity": {
        "__init__.py": """import os
import json
from azure.storage.blob import BlobServiceClient
from azure.identity import ManagedIdentityCredential

async def main(request_data: dict) -> dict:
    try:
        # Initialize BlobServiceClient
        container_name = os.environ.get("BLOB_STORAGE_CONTAINER_NAME_OIMS")
        blob_service_client = BlobServiceClient(
            os.environ.get("BLOB_STORAGE_ACCOUNT_URL"), 
            credential=ManagedIdentityCredential()
        )

        container_client = blob_service_client.get_container_client(container_name)
        blob_list = container_client.list_blobs()

        files = []
        for blob in blob_list:
            files.append({
                "file_name": blob.name,
                "size_in_bytes": blob.size,
                "last_modified": str(blob.last_modified)
            })

        # Return the list of files
        return {
            "status": "success",
            "files": files
        }
    
    except Exception as e:
        return {
            "status": "fail",
            "message": str(e)
        }
""",
        "function.json": """{
  "bindings": [
    {
      "name": "request_data",
      "type": "activityTrigger",
      "direction": "in"
    }
  ]
}
"""
    },
    "BlobDownloadActivity": {
        "__init__.py": """import os
import re
from azure.storage.blob.aio import BlobServiceClient
from azure.identity.aio import ManagedIdentityCredential
from datetime import datetime

async def main(request_data: dict) -> dict:
    try:
        # Extract file name from request
        file_name = request_data.get('name')
        if not file_name:
            return {
                "status": "fail",
                "message": "No file name provided"
            }

        # Initialize BlobServiceClient
        container_name = os.environ.get("BLOB_STORAGE_CONTAINER_NAME_OIMS")
        blob_service_client = BlobServiceClient(
            os.environ.get("BLOB_STORAGE_ACCOUNT_URL"), 
            credential=ManagedIdentityCredential()
        )

        # Attempt to download the file
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)

        if not await blob_client.exists():
            return {
                "status": "fail",
                "message": "File not found"
            }

        # Download the blob content
        downloader = await blob_client.download_blob()
        file_content = await downloader.content_as_bytes()

        return {
            "status": "success",
            "file_content": file_content.decode('utf-8')
        }
    
    except Exception as e:
        return {
            "status": "fail",
            "message": str(e)
        }
""",
        "function.json": """{
  "bindings": [
    {
      "name": "request_data",
      "type": "activityTrigger",
      "direction": "in"
    }
  ]
}
"""
    },
    "DurableHttpStart": {
        "__init__.py": """import azure.functions as func
import azure.durable_functions as df
import logging
import json

async def main(req: func.HttpRequest, starter: str) -> func.HttpResponse:
    client = df.DurableOrchestrationClient(starter)

    try:
        # Parse the request body for action and file parameters
        req_body = req.get_json()

        # Start the orchestration
        instance_id = await client.start_new("orchestrator_function", None, req_body)
        logging.info(f"Started orchestration with ID = '{instance_id}'.")

        # Wait for the orchestration to complete and return the result
        result = await client.wait_for_completion_or_create_check_status_response(req, instance_id)
        return result

    except ValueError:
        return func.HttpResponse(
            "Invalid request body",
            status_code=400
        )
""",
        "function.json": """{
  "bindings": [
    {
      "authLevel": "anonymous",
      "type": "httpTrigger",
      "direction": "in",
      "name": "req",
      "methods": ["post"],
      "route": null
    },
    {
      "type": "http",
      "direction": "out",
      "name": "$return"
    },
    {
      "name": "starter",
      "type": "durableClient",
      "direction": "in"
    }
  ]
}
"""
    }
}

# Create the folder structure and files
for folder, files in folders_and_files.items():
    os.makedirs(folder, exist_ok=True)  # Create the folder
    for file_name, file_content in files.items():
        file_path = os.path.join(folder, file_name)
        with open(file_path, "w") as f:
            f.write(file_content)

print("Folder structure and files have been generated.")
