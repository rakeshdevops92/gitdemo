import azure.functions as func
import azure.durable_functions as df
import logging
import json

async def main(req: func.HttpRequest, starter: str) -> func.HttpResponse:
    client = df.DurableOrchestrationClient(starter)

    try:
        req_body = req.get_json()

        instance_id = await client.start_new("orchestrator_function", None, req_body)
        logging.info(f"Started orchestration with ID = '{instance_id}'.")

        result = await client.wait_for_completion_or_create_check_status_response(req, instance_id)
        return result

    except ValueError:
        return func.HttpResponse(
            "Invalid request body",
            status_code=400
        )
