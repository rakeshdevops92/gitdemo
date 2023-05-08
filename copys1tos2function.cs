using System.IO;
using Microsoft.Azure.WebJobs;
using Microsoft.Extensions.Logging;
using Azure.Storage.Blobs;

namespace CopyBlobFunction
{
    public static class Function1
    {
        // The BlobTrigger attribute specifies that this function should be triggered
        // whenever a new blob is added to the "source-container" container in the
        // storage account specified in the "AzureWebJobsStorage" connection string.
        // The name of the blob is passed as a parameter to the function.
        [FunctionName("Function1")]
        public static void Run(
            [BlobTrigger("source-container/{name}", Connection = "AzureWebJobsStorage")] Stream myBlob,
            string name,
            ILogger log)
        {
            // Log information about the processed blob, including its name and size.
            log.LogInformation($"C# Blob trigger function processed blob\n Name:{name}\n  Size: {myBlob.Length} Bytes");

            // Retrieve the connection string for the destination storage account from
            // environment variables and use it to create a BlobServiceClient instance.
            string destinationStorageAccountConnectionString = $"DefaultEndpointsProtocol=https;AccountName={System.Environment.GetEnvironmentVariable("DESTINATION_STORAGE_ACCOUNT_NAME")};AccountKey={System.Environment.GetEnvironmentVariable("DESTINATION_STORAGE_ACCOUNT_KEY")};EndpointSuffix=core.windows.net";
            BlobServiceClient destinationBlobServiceClient = new BlobServiceClient(destinationStorageAccountConnectionString);

            // Get a reference to the destination container in the destination storage account.
            // If the container does not exist, create it.
            BlobContainerClient destinationContainerClient = destinationBlobServiceClient.GetBlobContainerClient("destination-container");
            destinationContainerClient.CreateIfNotExists();

            // Get a reference to the destination blob with the same name as the source blob.
            BlobClient destinationBlobClient = destinationContainerClient.GetBlobClient(name);

            // Upload the contents of the source blob to the destination blob.
            // If a blob with the same name already exists in the destination container,
            // overwrite it.
            destinationBlobClient.Upload(myBlob, overwrite: true);

            // Log a message indicating that the blob has been copied to the destination container.
            log.LogInformation("Blob has been copied to the destination container.");
        }
    }
}
