import logging
import requests
import os
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # List of endpoints to check
    endpoints = [
        "https://s3.us-south.cloud-object-storage.appdomain.cloud",
        "http://vz-proxy.pncint.net:80"
    ]
    
    # Validate endpoints
    results = {}
    for endpoint in endpoints:
        try:
            response = requests.get(endpoint, timeout=10)
            results[endpoint] = f"Allowed (Status Code: {response.status_code})"
        except requests.exceptions.RequestException as e:
            results[endpoint] = f"Blocked or unreachable ({str(e)})"
    
    return func.HttpResponse(str(results), status_code=200)

