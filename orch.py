import azure.durable_functions as df
from logging import INFO, getLogger
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor()
logger = getLogger(__name__)
logger.setLevel(INFO)

def BlobOrchestrator(context: df.DurableOrchestrationContext):
    input_data = context.get_input()
    action = input_data["action"]
    filepath = input_data.get("filepath", None)

    if action == "list":
        logger.info(f"Starting listing of blobs")
        result = yield context.call_activity("BlobListActivity", {})
    elif action == "download":
        logger.info(f"Starting download for filepath: {filepath}")
        result = yield context.call_activity("BlobDownloadActivity", {"filepath": filepath})

    return result

main = df.Orchestrator.create(BlobOrchestrator)
