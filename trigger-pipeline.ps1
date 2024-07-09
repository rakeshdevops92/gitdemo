param(
    [string]$organization,
    [string]$project,
    [string]$pipelineId,
    [string]$pat,
    [string]$branch,
    [string]$regions,
    [bool]$enforceManualValidation
)

$base64AuthInfo = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(":$($pat)"))

$uri = "https://dev.azure.com/$organization/$project/_apis/pipelines/$pipelineId/runs?api-version=7.1-preview.1"

$body = @{
    resources = @{
        repositories = @{
            self = @{
                refName = "refs/heads/$branch"
            }
        }
    }
    templateParameters = @{
        regions = $regions
        enforceManualValidation = [System.Convert]::ToBoolean($enforceManualValidation)
    }
} | ConvertTo-Json -Depth 10

$response = Invoke-RestMethod -Uri $uri -Method Post -Body $body -ContentType "application/json" -Headers @{Authorization=("Basic {0}" -f $base64AuthInfo)}

$response
