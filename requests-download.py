import requests

url = "https://s3.us-south.cloud-object-storage.appdomain.cloud/pnc-temp-retrieval-bkt-ritm3590766-04-29-2024/mongodb/maverick-transactions/Transactions.archive?AWSAccessKeyId=883a402c51dc4c5a98f8239623fed&Signature=0%2B2dxgHLXSZedL0TGJKDqapuA%2FJ3D%3D&Expires=1715106286"

output_file_path = "C:/Users/pj72963/Downloads/Transactions.archive"

response = requests.get(url, stream=True, verify=False)

if response.status_code == 200:
    with open(output_file_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    print(f"File downloaded successfully and saved to {output_file_path}")
else:
    print(f"Failed to download file: {response.status_code}")
