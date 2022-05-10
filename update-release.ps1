Param(
   [string]$collectionurl = "https://vsrm.dev.azure.com",
   [string] $org = "ORG",
   [string]$projectName = "DevOps",
   [string]$user = "test@test.com",
   [string]$token = "PAT",
   [int]$releasedId = 132, 
   [string]$var1 = "",
   [string]$var2 = ""

)

# Base64-encodes the Personal Access Token (PAT) appropriately
$base64AuthInfo = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(("{0}:{1}" -f $user,$token)))

$releaseUri = "$($collectionurl)/$org/$($projectName)/_apis/Release/releases/" + $releasedId + "?"
$result = Invoke-RestMethod -Uri $releaseUri -Method Get -ContentType "application/json" -Headers @{Authorization=("Basic {0}" -f $base64AuthInfo)}
#Write-Host "Environment name is " $result.environments
$envId = $result.environments.id

function CreateJsonBody
{
    $value = 
@"
{
      "status": "inProgress",
      "scheduledDeploymentTime": null,
      "comment": null,
      "variables": {
            "stage": {
                  "value":"test",
                  "allowOverride": true
            }
      }
}
"@

return $value
}
$json = CreateJsonBody
$envUri = "$($collectionurl)/$org/$($projectName)/_apis/Release/releases/" + $releasedId + "/environments/" + $envId + "?api-version=6.0-preview.6"
Write-Host $envUri
$result = Invoke-RestMethod -Uri $envUri -Method patch -Body $json -ContentType "application/json" -Headers @{Authorization=("Basic {0}" -f $base64AuthInfo)}
