import azure.durable_functions as df
from logging import INFO, getLogger
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor()
logger = getLogger(__name__)
logger.setLevel(INFO)

def PostOIMOrchestrator(context: df.DurableOrchestrationContext):
    input_data = context.get_input()
    blob_name = input_data["blob_name"]
    filepath = input_data["filepath"]

    logger.info(f"Starting activity for blob_name: {blob_name} from filepath: {filepath}")
    
    result = yield context.call_activity("OnpremtoAzure_Test_Activity", {"blob_name": blob_name, "filepath": filepath})
    return result

main = df.Orchestrator.create(PostOIMOrchestrator)
