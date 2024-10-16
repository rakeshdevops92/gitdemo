import azure.durable_functions as df

def orchestrator_function(context: df.DurableOrchestrationContext):
    input_data = context.get_input()
    blob_name = input_data['blob_name']
    fileByteArray = input_data['fileByteArray']

    result = yield context.call_activity("UploadBlobFromPremToAzure", {"blob_name": blob_name, "fileByteArray": fileByteArray})

    return result

main = df.Orchestrator.create(orchestrator_function)
