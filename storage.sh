#!/bin/bash

STORAGE_ACCOUNT_NAME=$AZURE_STORAGE_ACCOUNT_NAME
CONTAINER_NAME=$AZURE_STORAGE_CONTAINER_NAME
LOCAL_FILE_PATH=$AZURE_LOCAL_FILE_PATH
BLOB_NAME=$AZURE_BLOB_NAME

echo "Uploading $LOCAL_FILE_PATH to container $CONTAINER_NAME in storage account $STORAGE_ACCOUNT_NAME..."

az storage blob upload \
  --account-name $STORAGE_ACCOUNT_NAME \
  --container-name $CONTAINER_NAME \
  --name $BLOB_NAME \
  --file $LOCAL_FILE_PATH

if [ $? -eq 0 ]; then
    echo "File uploaded successfully!"
else
    echo "Failed to upload file."
    exit 1
fi
