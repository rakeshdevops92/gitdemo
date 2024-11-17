#!/bin/bash

# Logging function
log() {
    local level=$1
    local message=$2
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $message"
}

directory="/ark/landing_zone/manifest/metadata_json/"
start_major=3
start_minor=24
end_major=3
end_minor=26
matched_files=()

log "INFO" "Script execution started."

# Loop through files
for file in "$directory"/*; do
    filename=$(basename "$file")
    if [[ $filename =~ _Metadata([0-9]+)_([0-9]+)\.a360$ ]]; then
        major=${BASH_REMATCH[1]}
        minor=${BASH_REMATCH[2]}
        if (( major >= start_major && major <= end_major && minor >= start_minor && minor <= end_minor )); then
            matched_files+=("$filename")
        fi
    fi
done

if [ ${#matched_files[@]} -eq 0 ]; then
    log "WARN" "No matching files found for the given range."
    exit 1
fi

log "INFO" "Matching files: ${matched_files[*]}"

# Process matched files
for file in "${matched_files[@]}"; do
    full_path="$directory$file"
    log "INFO" "Processing file: $full_path"

    # Example operation (e.g., upload to Azure)
    curl -X POST "https://your-api-endpoint?file=$file" \
        -F "file=@$full_path" \
        -H "accept: application/json" \
        --cert "/path/to/cert.pem" --pass "yourpassword"

    if [ $? -ne 0 ]; then
        log "ERROR" "Failed to process file: $file"
    else
        log "INFO" "Successfully processed file: $file"
    fi
done

log "INFO" "Script execution completed."
