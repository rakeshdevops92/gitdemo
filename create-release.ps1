Param(
   [string]$collectionurl = "https://vsrm.dev.azure.com",
   [string] $org = "ORG",
   [string]$projectName = "DevOps",
   [string]$user = "YOUR-EMAIL",
   [string]$token = "YOUR-TOKEN",
   [string]$releasedDefinitionId = "15", 
   [string]$var1 = "Loreum",
   [string]$var2 = "Ipsum"

)

# Base64-encodes the Personal Access Token (PAT) appropriately
$base64AuthInfo = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(("{0}:{1}" -f $user,$token)))

function CreateJsonBody
{
    $value = @"
{
 "definitionId":$releasedDefinitionId,
 "variables": {
      "var1": {
            "value":"$var1",
            "allowOverride": true
      },
      "var2": {
            "value":"$var2",
            "allowOverride": true
      }
 },
 "isDraft":false,
 "reason": "none",
 "manualEnvironments":[] 
}
"@

 return $value
}

$json = CreateJsonBody

$uri = "$($collectionurl)/$org/$($projectName)/_apis/Release/releases?api-version=6.0"
$result = Invoke-RestMethod -Uri $uri -Method Post -Body $json -ContentType "application/json" -Headers @{Authorization=("Basic {0}" -f $base64AuthInfo)}
Write-Host "Created release" $result.name
