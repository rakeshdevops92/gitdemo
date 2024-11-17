import os
import re

def get_files_in_range(directory, start_range, end_range):
    matched_files = []
    start_major, start_minor = map(int, start_range.split('-'))
    end_major, end_minor = map(int, end_range.split('-'))

    for file in os.listdir(directory):
        match = re.search(r'_Metadata(\d+)_(\d+)\.a360$', file)
        if match:
            major, minor = map(int, match.groups())
            if start_major <= major <= end_major and start_minor <= minor <= end_minor:
                matched_files.append(file)

    return matched_files

directory_path = "/ark/landing_zone/manifest/metadata_json/AZL/"
start_range = "3-24"
end_range = "3-26"
matching_files = get_files_in_range(directory_path, start_range, end_range)

for file in matching_files:
    print(file)
