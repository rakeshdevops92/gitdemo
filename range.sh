#!/bin/bash

get_files_in_range() {
    local directory="$1"
    local start_range="$2"
    local end_range="$3"
    local matched_files=()

    IFS='-' read -r start_major start_minor <<< "$start_range"
    IFS='-' read -r end_major end_minor <<< "$end_range"

    for file in "$directory"/*; do
        if [[ "$file" =~ _Metadata([0-9]+)_([0-9]+)\.a360$ ]]; then
            major="${BASH_REMATCH[1]}"
            minor="${BASH_REMATCH[2]}"
            if (( start_major <= major && major <= end_major && start_minor <= minor && minor <= end_minor )); then
                matched_files+=("$file")
            fi
        fi
    done

    echo "${matched_files[@]}"
}

# Set directory and range
directory_path="/ark/landing_zone/manifest/metadata_json/AZL/"
start_range="3-24"
end_range="3-26"

# Call the function and print matching files
matching_files=$(get_files_in_range "$directory_path" "$start_range" "$end_range")

for file in $matching_files; do
    echo "$file"
done
