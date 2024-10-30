import azure.durable_functions as df
from logging import INFO, getLogger
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor()
logger = getLogger(__name__)
logger.setLevel(INFO)

def BlobOrchestrator(context: df.DurableOrchestrationContext):
    try:
        input_data = context.get_input()
        action = input_data.get("action")
        filepath = input_data.get("filepath", None)

        if action == "list":
            logger.info(f"Starting listing of blobs")
            result = yield context.call_activity("BlobListActivity", {})
        elif action == "download":
            logger.info(f"Starting download for filepath: {filepath}")
            result = yield context.call_activity("BlobDownloadActivity", {"filepath": filepath})
        else:
            result = {"status": "failed", "message": "Invalid action provided"}
            logger.error(f"Invalid action: {action}")

    except Exception as e:
        logger.error(f"Error in orchestrator: {str(e)}")
        result = {"status": "failed", "message": str(e)}  # Ensure result is assigned

    return result

main = df.Orchestrator.create(BlobOrchestrator)
