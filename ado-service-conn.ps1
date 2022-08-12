[cmdletbinding()]
param(
    [parameter(Mandatory = $true)]
    [ValidateNotNullorEmpty()]
    [string]$AzServicePrincipalId,

    [parameter(Mandatory = $true)]
    [ValidateNotNullorEmpty()]
    [string]$AzServicePrincipalKey,

    [parameter(Mandatory = $true)]
    [ValidateScript( { Get-AzSubscription -SubscriptionName $_ })]
    [string]$AzSubscriptionName,

    [parameter(Mandatory = $true)]
    [ValidateNotNullorEmpty()]
    [string]$AzDoOrganizationName,

    [parameter(Mandatory = $true)]
    [ValidateNotNullorEmpty()]
    [string]$AzDoProjectName,

    [parameter(Mandatory = $false)]
    [ValidateNotNullorEmpty()]
    [string]$AzDoConnectionName,

    [parameter(Mandatory = $false)]
    [ValidateNotNullorEmpty()]
    [string]$AzDoUserName,

    [parameter(Mandatory = $true)]
    [ValidateNotNullorEmpty()]
    [string]$AzDoToken
)

Write-Verbose "Starting Function New-AzDoServiceConnection"

# Create the header to authenticate to Azure DevOps
$base64AuthInfo = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(("{0}:{1}" -f $AzDoUserName, $AzDoToken)))
$Header = @{
    Authorization = ("Basic {0}" -f $base64AuthInfo)
}
Remove-Variable AzDoToken
try {
    $AzSubscription = Get-AzSubscription -SubscriptionName $AzSubscriptionName -ErrorAction Stop
}
Catch {
    Throw "Could not find subscription $AzSubscriptionName. Please verify it exists"
}
$AzSubscriptionID = $AzSubscription.Id
$TenantId = $AzSubscription.TenantId

## Get ProjectId
$URL = "https://dev.azure.com/$AzDoOrganizationName/_apis/projects?api-version=6.0"
Try {
    $AzDoProjectNameproperties = (Invoke-RestMethod $URL -Headers $Header -ErrorAction Stop).Value
    Write-Verbose "Collected Azure DevOps Projects"
}
Catch {
    if ($_ | Select-String -Pattern "Access Denied: The Personal Access Token used has expired.") {
        Throw "Access Denied: The Azure DevOps Personal Access Token used has expired."
    }
    else {
        $ErrorMessage = $_ | ConvertFrom-Json
        Throw "Could not collect project: $($ErrorMessage.message)"
    }
}
$AzDoProjectID = ($AzDoProjectNameproperties | Where-Object { $_.Name -eq $AzDoProjectName }).id
Write-Verbose "Collected ID: $AzDoProjectID"

# Create body for the API call
$Body = @{
    data                             = @{
        subscriptionId   = $AzSubscriptionID
        subscriptionName = $AzSubscriptionName
        environment      = "AzureCloud"
        scopeLevel       = "Subscription"
        creationMode     = "Manual"
    }
    name                             = ($AzSubscriptionName -replace " ")
    type                             = "AzureRM"
    url                              = "https://management.azure.com/"
    authorization                    = @{
        parameters = @{
            tenantid            = $TenantId
            serviceprincipalid  = $AzServicePrincipalId
            authenticationType  = "spnKey"
            serviceprincipalkey = $AzServicePrincipalKey
        }
        scheme     = "ServicePrincipal"
    }
    isShared                         = $false
    isReady                          = $true
    serviceEndpointProjectReferences = @(
        @{
            projectReference = @{
                id   = $AzDoProjectID
                name = $AzDoProjectName
            }
            name             = $AzDoConnectionName
        }
    )
}
Remove-Variable AzServicePrincipalKey
$URL = "https://dev.azure.com/$AzDoOrganizationName/$AzDoProjectName/_apis/serviceendpoint/endpoints?api-version=6.0-preview.4"
$Parameters = @{
    Uri         = $URL
    Method      = "POST"
    Body        = ($Body | ConvertTo-Json -Depth 3)
    Headers     = $Header
    ContentType = "application/json"
    Erroraction = "Stop"
}
try {
    Write-Verbose "Creating Connection"
    $Result = Invoke-RestMethod @Parameters
}
Catch {
    $ErrorMessage = $_ | ConvertFrom-Json
    Throw "Could not create Connection: $($ErrorMessage.message)"
}
Write-Verbose "Connection Created"
$Result
