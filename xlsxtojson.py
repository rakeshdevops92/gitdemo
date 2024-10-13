import os
import pandas as pd
import json
import hashlib
import openpyxl

# Source and destination directories (modify these as necessary)
src_dir = "/home/pk45295/metadata_excel/"
dest_dir = "/home/pk45295/metadata_json/"

def exceltojson():
    for filename in os.listdir(src_dir):
        if filename.endswith(".xlsx"):
            excel_filename = os.path.join(src_dir, filename)
            print(f"Processing xlsx filename: {excel_filename}")

            newWorkbook = openpyxl.load_workbook(excel_filename)

            Worksheet = newWorkbook["mapping"]

            count = -2  # Initialize count
            for column_data in Worksheet['L']:  # Assuming column L has relevant data
                filename = os.path.basename(column_data.value)
                pathname = os.path.dirname(column_data.value)
                file_extension = os.path.splitext(column_data.value)[1].strip()
                new_extension = ".json"
                base, extension = os.path.splitext(filename)
                json_file_name = base + new_extension

                hash_text = json_file_name
                hash_object = hashlib.md5(hash_text.encode())
                relation_id = hash_object.hexdigest()

                print(f"Creating json for filename = {json_file_name}")
                print(f"relation_id (Unique value) = {relation_id}")

                excel_data_df = pd.read_excel(excel_filename, sheet_name='mapping')

                json_excel_str = excel_data_df.to_json(orient='records', date_format='iso')
                json_excel = json.loads(json_excel_str)

                json_first = {
                    "operation": "create_record",
                    "relation_id": relation_id,
                    "record_metadata": json_excel[count]  # Assuming row corresponds to the data
                }

                json_first_final = [json_first]
                with open(os.path.join(dest_dir, json_file_name), 'w') as file:
                    json.dump(json_first_final, file, indent=4)

                json_second_list = []
                with open(os.path.join(dest_dir, json_file_name), 'r') as fp:
                    json_second_list = json.load(fp)

                json_excel_two = pd.read_excel(excel_filename, sheet_name='mapping').to_json(orient='records', date_format='iso')
                json_excel_two = json.loads(json_excel_two)

                json_second_list.append({
                    "operation": "upload_new_file",
                    "relation_id": relation_id,
                    "file_metadata": json_excel_two[count]
                })

                with open(os.path.join(dest_dir, json_file_name), 'w') as json_file:
                    json.dump(json_second_list, json_file, indent=4)

                print(f"Created JSON file: {json_file_name}")
                count += 1

exceltojson()
