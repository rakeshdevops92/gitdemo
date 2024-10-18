import logging
import azure.durable_functions as df

def PostOIMOrchestrator(context: df.DurableOrchestrationContext):
    input_data = context.get_input()

    blob_name = input_data["blob_name"]
    filepath = input_data["filepath"]

    logging.info(f"Starting activity for blob_name: {blob_name} from filepath: {filepath}")

    result = yield context.call_activity("UploadBlobFromPremToAzure", {"blob_name": blob_name, "filepath": filepath})
    return result

main = df.Orchestrator.create(PostOIMOrchestrator)
