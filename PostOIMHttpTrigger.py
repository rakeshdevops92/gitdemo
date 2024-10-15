import azure.functions as func
import azure.durable_functions as df
import logging

async def main(req: func.HttpRequest, starter: str) -> func.HttpResponse:
    blob_name = ""
    timeStartPost = ""
    fileByteArray = None
    try:
        filepath = req.params.get('filepath')
        for key, value in req.files.items():
            if filepath and filepath != "":
                blob_name = filepath
            else:
                blob_name = key

            timeStartPost = datetime.utcnow().isoformat(sep=".", timespec="milliseconds")
            logging.info(f"Start Post File {blob_name} at {timeStartPost}")
            fileByteArray = value.stream.read()

        client = df.DurableOrchestrationClient(starter)
        instance_id = await client.start_new("PostOIMOrchestrator", None, {"blob_name": blob_name, "fileByteArray": fileByteArray})

        logging.info(f"Started orchestration with ID = '{instance_id}'.")
        return client.create_check_status_response(req, instance_id)

    except Exception as ex:
        logging.error(f"Error: {str(ex)}")
        return func.HttpResponse(f"Error: {str(ex)}", status_code=500)
