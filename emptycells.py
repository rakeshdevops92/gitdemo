def process_excel_file(self):
    self.logger.info(f"=== Starting to process Excel file: {self.input_file} ===\n")

    if self.check_previous_conversion():
        return

    try:
        wb = load_workbook(self.input_file, data_only=True)
    except Exception as e:
        self.logger.error(f"Error loading workbook: {e}")
        sys.exit(1)

    excel_base_name = os.path.splitext(os.path.basename(self.input_file))[0]
    file_count = 0
    total_upload_operations = 0
    metadata_sheets = [sheet for sheet in wb.sheetnames if sheet.startswith("Metadata")]

    if not metadata_sheets:
        self.logger.error("No metadata sheets found in the workbook!")
        sys.exit(1)

    self.logger.info(f"Found {len(metadata_sheets)} metadata sheet(s) to process\n")

    for sheet_name in metadata_sheets:
        self.logger.info(f"\nProcessing sheet: {sheet_name}")
        sheet = wb[sheet_name]
        current_records = []
        records_per_file = 5000

        required_cells = ["B1", "B4", "C9", "D1", "D3", "B2", "D2", "B3"]
        for cell in required_cells:
            if not sheet[cell].value:
                self.logger.error(f"Missing required value in sheet '{sheet_name}', cell '{cell}'")
                sys.exit(1)

        publisher = sheet["B1"].value
        region = sheet["B4"].value
        record_class = sheet["C9"].value
        provenance = sheet["D1"].value
        security_classification = sheet["D3"].value
        creator = sheet["B2"].value
        contributor = sheet["D2"].value
        cost_center = str(sheet["B3"].value).zfill(12) if isinstance(sheet["B3"].value, (int, float)) else sheet["B3"].value.strip()

        file_counter = 1
        row_count = 0

        for row in sheet.iter_rows(min_row=9, values_only=True):
            if row[0] is None:
                break
            row_count += 1

            for col_index, cell_value in enumerate(row[:9]):
                if cell_value is None:
                    col_letter = chr(65 + col_index)  # Get column letter (A, B, C, etc.)
                    self.logger.error(f"Missing value in sheet '{sheet_name}', row {row_count + 8}, column {col_letter}")
                    sys.exit(1)

            file_name = row[0]
            file_path = row[1]
            folder_path = f"/dropzone/a360root/{publisher.lower()}/submission/{file_path}/"
            record_code = row[2]
            record_date = row[3]
            formatted_record_date = self.format_iso_date(record_date)
            relation_id = str(uuid.uuid4())
            submission_date = datetime.now().isoformat() + "-05:00"

            record_metadata = {
                "record_class": record_class,
                "publisher": publisher,
                "region": region,
                "recordDate": formatted_record_date,
                "provenance": provenance,
                "submission_date": submission_date,
                "security_classification": security_classification,
                "contributor": contributor,
                "creator": creator,
                "description": row[4],
                "title": file_name,
                "language": "eng",
                "cost_center": cost_center,
                "date_range": row[5],
                "major_description": row[6],
                "minor_description": row[7],
                "reference_1": row[8],
            }

            file_metadata = {
                "publisher": publisher,
                "source_folder_path": file_path,
                "source_file_name": file_name,
                "dz_folder_path": folder_path,
                "dz_file_name": file_name,
                "file_tag": self.get_file_tag(file_name),
            }

            current_records.append({"operation": "create_record", "relation_id": relation_id, "record_metadata": record_metadata})
            current_records.append({"operation": "upload_new_file", "relation_id": relation_id, "file_metadata": file_metadata})

            if len(current_records) >= records_per_file * 2:
                output_file_path = os.path.join(
                    self.output_directory,
                    f"{excel_base_name}_{sheet_name}_{file_counter}.a360"
                )
                upload_count = self.write_records_to_file(output_file_path, current_records, sheet_name)
                total_upload_operations += upload_count
                current_records = []
                file_counter += 1
                file_count += 1

        if current_records:
            output_file_path = os.path.join(
                self.output_directory,
                f"{excel_base_name}_{sheet_name}_{file_counter}.a360"
            )
            upload_count = self.write_records_to_file(output_file_path, current_records, sheet_name)
            total_upload_operations += upload_count
            file_count += 1

        self.logger.info(f"\n=== Processing Complete ===")
        self.logger.info(f"Total manifest files created: {file_count}")
        self.logger.info(f"Total upload_new_file operations: {total_upload_operations}")

        self.record_conversion()
