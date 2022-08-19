storage_account_name = "teststgdl"
client_id = dbutils.secrets.get(scope="formula1-scope", key="db-app-client-id")
tenant_id = dbutils.secrets.get(scope="formula1-scope", key="db-tenant-id")
client_secret = dbutils.secrets.get(scope="formula1-scope", key="db-client-secret")
container_name = "raw"
configs = {"fs.azure.account.auth.type": "OAuth",
           "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
           "fs.azure.account.oauth2.client.id": f"{client_id}",
           "fs.azure.account.oauth2.client.secret": f"{client_secret}",
           "fs.azure.account.oauth2.client.endpoint": f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"
          }

def mount_adls(containername):
    dbutils.fs.mount(
      source = f"abfss://{containername}@{storage_account_name}.dfs.core.windows.net",
      mount_point = f"/mnt/{storage_account_name}/{containername}",
      extra_configs = configs)

 mount_adls(container_name)
