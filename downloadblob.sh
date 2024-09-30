STORAGE_ACCOUNT_NAME="${storageAccountName}"
CONTAINER_NAME="test"
STORAGE_ACCOUNT_KEY="${storageAccountKey}"
BLOB_NAME="config.xml"                 # Name of the file in the storage container
LOCAL_PATH="/path/to/config.xml"        # Path to place the file on the VM

# Download config.xml from the storage account to the VM
echo "Downloading config.xml from the storage account..."
az vm run-command invoke \
  --resource-group ${midrgname} \
  --name ${midvmname} \
  --command-id RunShellScript \
  --scripts "sudo su && az storage blob download --account-name ${STORAGE_ACCOUNT_NAME} --account-key '${STORAGE_ACCOUNT_KEY}' --container-name ${CONTAINER_NAME} --name ${BLOB_NAME} --file ${LOCAL_PATH}"

if [ $? -eq 0 ]; then
  echo "File downloaded successfully to ${LOCAL_PATH}!"
  echo "Starting the service using start.sh..."
    az vm run-command invoke \
      --resource-group ${midrgname} \
      --name ${midvmname} \
      --command-id RunShellScript \
      --scripts "sudo su && cd /opt/servicenow/mid/agent && ./start.sh"

    if [ $? -eq 0 ]; then
      echo "Service started successfully!"
    else
      echo "Failed to start the service."
      exit 1
    fi
else
  echo "File download failed."
  exit 1
fi
