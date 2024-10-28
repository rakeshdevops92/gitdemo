
import logging
import azure.durable_functions as df
from opentelemetry import trace
from opentelemetry.instrumentation.logging import LoggingInstrumentor

LoggingInstrumentor().instrument(set_logging_format=True)
tracer = trace.get_tracer(__name__)

def PostOIMOrchestrator(context: df.DurableOrchestrationContext):
    input_data = context.get_input()
    blob_name = input_data["blob_name"]
    filepath = input_data["filepath"]

    with tracer.start_as_current_span("durable_function_orchestrator"):
        logging.info(f"Starting activity for blob_name: {blob_name} from filepath: {filepath}")

    result = yield context.call_activity("OnpremtoAzure_Test_Activity", {"blob_name": blob_name, "filepath": filepath})
    return result

main = df.Orchestrator.create(PostOIMOrchestrator)
