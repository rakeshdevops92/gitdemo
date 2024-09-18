inlineScript: |
      az vm run-command invoke \
        --resource-group $(VM_RESOURCE_GROUP) \
        --name $(VM_NAME) \
        --command-id RunShellScript \
        --scripts 'sudo su && cd /opt/servicenow/mid/agent && az storage blob upload --account-name $(STORAGE_ACCOUNT_NAME) --account-key $(STORAGE_ACCOUNT_KEY) --container-name $(CONTAINER_NAME) --name $(BLOB_NAME) --file ./config.xml'

      if [ $? -eq 0 ]; then
        echo "File uploaded successfully!"
      else
        echo "File upload failed."
        exit 1
      fi
