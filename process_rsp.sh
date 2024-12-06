#!/bin/bash

LOG_FILE="process_rsp.log"
JSON_FILE="Lists.txt"
CURL_COMMAND_BASE="curl -v -X GET 'https://func-ark-prod-aze2.azurewebsites.net/api/getfile?name=idf/response"
OUTPUT_DIRECTORY="/ark/landing_zone/idf/listing"
CERT_FILE="/ark/landing_zone/cert/azureappreg-ark-onprem-prod.pncint.net.pem"
CERT_PASS="Aopcc#24$"

jq -r '.[] | select(.name | endswith(".rsp")) | .name' "$JSON_FILE" | while read -r RSP_FILE; do
    OUTPUT_FILE="${OUTPUT_DIRECTORY}/$(basename "$RSP_FILE")"
    FULL_CURL_COMMAND="${CURL_COMMAND_BASE}/${RSP_FILE}' -H 'accept: application/json' --output '${OUTPUT_FILE}' --cert '${CERT_FILE}' --pass '${CERT_PASS}'"
    echo "$(date '+%Y-%m-%d %H:%M:%S') Executing: $FULL_CURL_COMMAND" >> "$LOG_FILE"
    eval $FULL_CURL_COMMAND >> "$LOG_FILE" 2>&1
    if [ $? -eq 0 ]; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') Successfully processed $RSP_FILE" >> "$LOG_FILE"
    else
        echo "$(date '+%Y-%m-%d %H:%M:%S') Failed to process $RSP_FILE" >> "$LOG_FILE"
    fi
done
