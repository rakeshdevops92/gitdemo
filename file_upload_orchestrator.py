from azure.durable_functions import DurableOrchestrationContext, Orchestrator

def file_upload_orchestrator(context: DurableOrchestrationContext):
    result = yield context.call_activity("upload_file_activity", context.get_input())
    return result

main = Orchestrator.create(file_upload_orchestrator)
