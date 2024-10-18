import azure.functions as func
import azure.durable_functions as df
import os
import logging

async def main(req: func.HttpRequest, starter: str):
    function_name = req.route_params.get('functionName')
    
    filepath = req.params.get('filepath')

    if not filepath:
        return func.HttpResponse("Filepath not provided", status_code=400)

    blob_name = os.path.basename(filepath)

    logging.info(f"Starting orchestration for blob_name={blob_name}, filepath={filepath}")

    client = df.DurableOrchestrationClient(starter)
    instance_id = await client.start_new(function_name, None, {"blob_name": blob_name, "filepath": filepath})
    response = client.create_check_status_response(req, instance_id)
    return response
