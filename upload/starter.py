import azure.functions as func
import azure.durable_functions as df
import os
from logging import INFO, getLogger
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor()
logger = getLogger(__name__)
logger.setLevel(INFO)

async def main(req: func.HttpRequest, starter: str):
    function_name = req.route_params.get('functionName')
    filepath = req.params.get('filepath')

    if not filepath:
        logger.error("Filepath not provided")
        return func.HttpResponse("Filepath not provided", status_code=400)

    blob_name = os.path.basename(filepath)
    logger.info(f"Starting orchestration for blob_name={blob_name}, filepath={filepath}")

    client = df.DurableOrchestrationClient(starter)
    instance_id = await client.start_new(function_name, None, {"blob_name": blob_name, "filepath": filepath})

    response = client.create_check_status_response(req, instance_id)
    return response
