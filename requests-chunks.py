import requests
import os

proxy = "http://vz-proxy.pncint.net:80"
os.environ["https_proxy"] = proxy

url = "https://s3.us-south.cloud-object-storage.appdomain.cloud/pnc-temp-ritm3627143-05-29-2024/NLD/NLD_11_03_2021.zip?AWSAccessKeyId=xxxxxxxxx&Signature=xxxxxx&Expires=xxxxxxxx"

output_file_path = "/home/pj72963/backup/NLD/NLD_11_03_2021.zip"

response = requests.get(url, stream=True, verify=False)
if response.status_code == 200:
    with open(output_file_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    print(f"File downloaded successfully and saved to {output_file_path}")
else:
    print(f"Failed to download file: {response.status_code}")
