import azure.functions as func
from azure.durable_functions import DurableOrchestrationClient

async def main(req: func.HttpRequest, starter: str) -> func.HttpResponse:
    client = DurableOrchestrationClient(starter)

    try:
        file_info = {}
        file_path = req.params.get('filepath')
        for key, value in req.files.items():
            file_info['blob_name'] = file_path or key
            file_info['file_byte_array'] = value.stream.read()

        instance_id = await client.start_new("file_upload_orchestrator", None, file_info)
        return client.create_check_status_response(req, instance_id)

    except Exception as e:
        return func.HttpResponse(f"Failed to start the durable function: {str(e)}", status_code=500)
