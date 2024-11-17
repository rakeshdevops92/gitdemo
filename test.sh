#!/bin/bash

log() {
    local level="$1"
    local message="$2"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $message"
}

get_files_in_range() {
    local directory="$1"
    local start_range="$2"
    local end_range="$3"
    local matched_files=()

    log "INFO" "Starting to process files in directory: $directory"
    log "INFO" "Looking for files in range: $start_range to $end_range"

    IFS='-' read -r start_major start_minor <<< "$start_range"
    IFS='-' read -r end_major end_minor <<< "$end_range"

    for file in "$directory"/*; do
        if [[ "$file" =~ _Metadata([0-9]+)_([0-9]+)\.a360$ ]]; then
            major="${BASH_REMATCH[1]}"
            minor="${BASH_REMATCH[2]}"
            log "DEBUG" "Processing file: $file (Major: $major, Minor: $minor)"
            if (( start_major <= major && major <= end_major && start_minor <= minor && minor <= end_minor )); then
                log "INFO" "File $file matches the range criteria"
                matched_files+=("$file")
            else
                log "DEBUG" "File $file does not match the range criteria"
            fi
        else
            log "WARNING" "File $file does not match the naming pattern"
        fi
    done

    log "INFO" "Finished processing files in directory: $directory"
    log "INFO" "Total matching files: ${#matched_files[@]}"

    echo "${matched_files[@]}"
}

directory_path="/ark/landing_zone/manifest/metadata_json/AZL/"
start_range="3-24"
end_range="3-26"

log "INFO" "Script execution started"

if [[ ! -d "$directory_path" ]]; then
    log "ERROR" "Directory does not exist: $directory_path"
    exit 1
fi

matching_files=$(get_files_in_range "$directory_path" "$start_range" "$end_range")

if [[ -z "$matching_files" ]]; then
    log "WARNING" "No files found matching the range $start_range to $end_range"
else
    log "INFO" "Matching files:"
    for file in $matching_files; do
        log "INFO" "$file"
    done
fi

log "INFO" "Script execution completed"
