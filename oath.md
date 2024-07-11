# Trigger Azure DevOps Pipeline Using AAD OAuth Token

This guide provides detailed steps to generate an OAuth token using PowerShell and use it to trigger an Azure DevOps pipeline.

## Prerequisites

- Azure Subscription
- Azure Active Directory (AAD) access
- Azure DevOps organization and project
- PowerShell installed on your machine

## Step 1: Register an Application in Azure AD

1. **Navigate to Azure AD**:
   - Go to the [Azure portal](https://portal.azure.com).
   - Navigate to "Azure Active Directory" > "App registrations".

2. **Register a New Application**:
   - Click on "New registration".
   - Name your application, select the supported account types (usually "Accounts in this organizational directory only"), and provide a redirect URI if needed.
   - Click "Register".

3. **Configure API Permissions**:
   - In the registered application, go to "API permissions".
   - Click "Add a permission".
   - Select "APIs my organization uses" and search for "Azure DevOps".
   - Select "Azure DevOps" and choose the appropriate permissions, such as `user_impersonation`.
   - Grant admin consent for the permissions.

4. **Generate a Client Secret**:
   - Go to "Certificates & secrets" in the registered application.
   - Click "New client secret", provide a description, and set an expiration period.
   - Note down the generated client secret.

## Step 2: Obtain an OAuth Token using PowerShell

Use the following PowerShell script to obtain an OAuth token:

```powershell
# Define your Azure AD Tenant ID, Client ID, Client Secret, and Resource URI
$tenantId = "<Your_Tenant_ID>"
$clientId = "<Your_Client_ID>"
$clientSecret = "<Your_Client_Secret>"
$resource = "https://dev.azure.com"

# Prepare the request body
$body = @{
    client_id     = $clientId
    scope         = "$resource/.default"
    client_secret = $clientSecret
    grant_type    = "client_credentials"
}

# Send the request to Azure AD to get the OAuth token
$response = Invoke-RestMethod -Method Post -Uri "https://login.microsoftonline.com/$tenantId/oauth2/v2.0/token" -ContentType "application/x-www-form-urlencoded" -Body $body

# Extract the token from the response
$token = $response.access_token

# Output the token
Write-Output "OAuth Token: $token"
