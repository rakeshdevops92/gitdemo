#!/bin/bash

LOG_FILE="/path/to/log_file.log"

TIMESTAMP=$(date +"%d%m%Y%H%M%S")

METADATA_FILE_BASE="response_files_list_${TIMESTAMP}.txt"
METADATA_FILE="/ark/landing_zone/idf/${METADATA_FILE_BASE}"
DEST_DIR_BASE="response_files_list_${TIMESTAMP}"
DEST_DIR="/ark/landing_zone/idf/${DEST_DIR_BASE}"

CERT_PATH="/ark/landing_zone/cert/azureappreg-ark-onprem-prod.pncint.net.pem"
PASS="Aopcc#24$"

mkdir -p "$DEST_DIR"

echo "$(date +"%Y-%m-%d %H:%M:%S") - Fetching metadata file: $METADATA_FILE_BASE" >> "$LOG_FILE"
curl -X 'GET' "https://func-ark-prod-aze2.azurewebsites.net/api/ARK_FileInfo_OnPrem?filenamestartswith=idf/response" \
    -H 'accept: application/json' \
    --cert "$CERT_PATH" \
    --pass "$PASS" \
    --output "$METADATA_FILE"

if [[ ! -f "$METADATA_FILE" ]]; then
    echo "$(date +"%Y-%m-%d %H:%M:%S") - Failed to download metadata file." >> "$LOG_FILE"
    exit 1
fi

echo "$(date +"%Y-%m-%d %H:%M:%S") - Successfully downloaded metadata file." >> "$LOG_FILE"

while IFS= read -r line; do
    file_path=$(echo "$line" | awk '{print $2}')
    
    if [[ "$file_path" =~ ^idf/response/[^/]+\.[^./]+$ ]]; then
        filename_only=$(basename "$file_path")
        
        echo "$(date +"%Y-%m-%d %H:%M:%S") - Downloading file: $filename_only to $DEST_DIR" >> "$LOG_FILE"
        curl -X 'GET' "https://func-ark-prod-aze2.azurewebsites.net/api/getfile?name=$file_path" \
            -H 'accept: application/json' \
            --output "${DEST_DIR}/${filename_only}" \
            --cert "$CERT_PATH" \
            --pass "$PASS"
        
        if [[ $? -eq 0 ]]; then
            echo "$(date +"%Y-%m-%d %H:%M:%S") - Successfully downloaded $filename_only" >> "$LOG_FILE"
        else
            echo "$(date +"%Y-%m-%d %H:%M:%S") - Failed to download $filename_only" >> "$LOG_FILE"
        fi
    else
        echo "$(date +"%Y-%m-%d %H:%M:%S") - Invalid file path format: $file_path" >> "$LOG_FILE"
    fi
done < "$METADATA_FILE"
