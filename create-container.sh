container_exists=$(az storage container exists \
    --name ${CONTAINER_NAME} \
    --account-name ${STORAGE_ACCOUNT_NAME} \
    --account-key "${STORAGE_ACCOUNT_KEY}" \
    --query "exists")

  if [ "${container_exists}" = "false" ]; then
    echo "Container does not exist. Creating container..."
    az storage container create \
      --name ${CONTAINER_NAME} \
      --account-name ${STORAGE_ACCOUNT_NAME} \
      --account-key "${STORAGE_ACCOUNT_KEY}"
    
    if [ $? -eq 0 ]; then
      echo "Container created successfully!"
    else
      echo "Failed to create container."
      exit 1
    fi
  else
    echo "Container already exists."
  fi
