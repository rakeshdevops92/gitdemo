$org = "your-org"
$repoList = @("repo1", "repo2", "repo3")
$token = "your-token"
$headers = @{
    Authorization = "Bearer $token"
    Accept = "application/vnd.github.v3+json"
}
$baseUrl = "https://github.your-company.com/api/v3/repos"

$filesToCreate = @{
    "CODEOWNERS" = @"
# CODEOWNERS file
* @team1
* @team2
"@

    "mergeable.yml" = @"
# Configuration for mergeability
mergeable:
  - when: pull_request.* 
    name: 'Check PR Label'
    validate:
      - do: label
        must_include:
          regex: '.*'
"@
}

foreach ($repo in $repoList) {
    foreach ($fileName in $filesToCreate.Keys) {
        $fileContent = $filesToCreate[$fileName]
        $encodedContent = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($fileContent))

        $fileUrl = "$baseUrl/$org/$repo/contents/.github/$fileName"

        # Check if file exists
        try {
            Invoke-RestMethod -Uri $fileUrl -Method Get -Headers $headers
            Write-Host "$fileName already exists in $repo. Skipping creation."
        } catch {
            if ($_.Exception.Response.StatusCode -eq 'NotFound') {
                # File does not exist, create it
                $body = @{
                    message = "Create $fileName"
                    content = $encodedContent
                } | ConvertTo-Json -Depth 5

                try {
                    Invoke-RestMethod -Uri $fileUrl -Method Put -Headers $headers -Body $body -ContentType "application/json"
                    Write-Host "Successfully created $fileName in $repo."
                } catch {
                    Write-Error "Failed to create $fileName in $repo: $_"
                }
            } else {
                Write-Error "Error checking existence of $fileName in $repo: $_"
            }
        }
    }
}
