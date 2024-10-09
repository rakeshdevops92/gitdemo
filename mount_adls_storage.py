 action = req.params.get('action')

        if not path and not action:
            try:
                req_body = req.get_json()
            except ValueError:
                pass
            else:
                path = req_body.get('name')
                action = req_body.get('action')

        # If action is 'list', list all files in the container
        if action == 'list':
            container_client = blobServiceClient.get_container_client(container_name)
            blob_list = container_client.list_blobs()
            
            files = []
            for blob in blob_list:
                files.append({
                    "file_name": blob.name,
                    "size_in_bytes": blob.size,
                    "last_modified": str(blob.last_modified)
                })

            return func.HttpResponse(
                json.dumps({"status": "success", "files": files}),
                status_code=200,
                mimetype='application/json'
            )
