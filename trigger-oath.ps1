param(
    [string]$organization,
    [string]$project,
    [string]$pipelineId,
    [string]$oauthToken,
    [string]$branch,
    [string]$regions,
    [bool]$enforceManualValidation
)

$uri = "https://dev.azure.com/$organization/$project/_apis/pipelines/$pipelineId/runs?api-version=7.1-preview.1"

# Prepare the request body
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
} | Convert-ToJson -Depth 10

$response = Invoke-RestMethod -Uri $uri -Method Post -Body $body -ContentType "application/json" -Headers @{Authorization = "Bearer $oauthToken"}

$response
