import logging
import requests
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
            if response.status_code >= 200 and response.status_code < 300:
                results[endpoint] = f"Accessible (Status Code: {response.status_code})"
            elif response.status_code >= 400 and response.status_code < 500:
                results[endpoint] = f"Client Error (Status Code: {response.status_code})"
            elif response.status_code >= 500 and response.status_code < 600:
                results[endpoint] = f"Server Error (Status Code: {response.status_code})"
            else:
                results[endpoint] = f"Other Status Code: {response.status_code}"
        except requests.exceptions.RequestException as e:
            results[endpoint] = f"Blocked or unreachable ({str(e)})"

    return func.HttpResponse(str(results), status_code=200)
