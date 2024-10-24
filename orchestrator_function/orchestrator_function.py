import azure.functions as func
import azure.durable_functions as df

def orchestrator_function(context: df.DurableOrchestrationContext):
    request_data = context.get_input()
    
    action = request_data.get('action')
    if action == 'list':
        # Call the blob listing activity
        result = yield context.call_activity('BlobListingActivity', request_data)
    else:
        # Call the file downloading activity
        result = yield context.call_activity('BlobDownloadActivity', request_data)
    
    return result

main = df.Orchestrator.create(orchestrator_function)
