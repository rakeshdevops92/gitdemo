import os
import pandas as pd
import json
import hashlib

src_file = "/home/pj72963/metadata_excel/Content_Metadata_by_Cost_Center.xlsx"
dest_file = "/home/pj72963/metadata_json/output.json"

def excel_to_json():
    df = pd.read_excel(src_file)
    
    metadata_keys = df.iloc[0:7, 0].values
    metadata_values = df.iloc[0:7, 1].values

    metadata = {metadata_keys[i]: metadata_values[i] for i in range(len(metadata_keys))}

    relation_id = hashlib.md5(str(metadata).encode()).hexdigest()

    df_files = pd.read_excel(src_file, skiprows=7)
    df_files.fillna("", inplace=True)

    json_output = []

    json_output.append({
        "operation": "create_record",
        "relation_id": relation_id,
        "record_metadata": metadata
    })

    for index, row in df_files.iterrows():
        file_metadata = {col_name: row[col_name] for col_name in df_files.columns}

        json_output.append({
            "operation": "upload_new_file",
            "relation_id": relation_id,
            "file_metadata": file_metadata
        })

    with open(dest_file, 'w') as json_file:
        json.dump(json_output, json_file, indent=4)

    print(f"JSON file created successfully at {dest_file}")

excel_to_json()
