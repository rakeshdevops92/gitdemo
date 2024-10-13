import os
import pandas as pd
import json
import hashlib

src_file = "/home/pj72963/metadata_excel/Content_Metadata_by_Cost_Center.xlsx"
dest_file = "/home/pj72963/metadata_json/output.json"

def excel_to_json():
    df = pd.read_excel(src_file, header=None)
    
    metadata = {}
    for i in range(df.shape[0]):
        if pd.isna(df.iloc[i, 0]) and pd.isna(df.iloc[i, 2]):
            break
        if pd.notna(df.iloc[i, 0]) and pd.notna(df.iloc[i, 1]):
            metadata[df.iloc[i, 0]] = df.iloc[i, 1]
        if pd.notna(df.iloc[i, 2]) and pd.notna(df.iloc[i, 3]):
            metadata[df.iloc[i, 2]] = df.iloc[i, 3]

    metadata = {k: v for k, v in metadata.items() if pd.notna(v)}

    relation_id = hashlib.md5(str(metadata).encode()).hexdigest()

    file_data_start_row = i + 2

    df_files = pd.read_excel(src_file, skiprows=file_data_start_row)
    df_files.fillna("", inplace=True)

    json_output = []

    json_output.append({
        "operation": "create_record",
        "relation_id": relation_id,
        "record_metadata": metadata
    })

    for index, row in df_files.iterrows():
        file_metadata = {col_name: row[col_name] for col_name in df_files.columns if pd.notna(row[col_name]) and row[col_name] != ""}
        
        if file_metadata:
            json_output.append({
                "operation": "upload_new_file",
                "relation_id": relation_id,
                "file_metadata": file_metadata
            })

    with open(dest_file, 'w') as json_file:
        json.dump(json_output, json_file, indent=4)

    print(f"JSON file created successfully at {dest_file}")

excel_to_json()
