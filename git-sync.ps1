$org = "your-org"
$repoList = @("repo1", "repo2", "repo3")
$filesToSync = @("CODEOWNERS", "mergeable.yml")
$token = "your-token"
$headers = @{
    Authorization = "Bearer $token"
    Accept = "application/vnd.github.v3+json"
}
$baseUrl = "https://github.your-company.com/api/v3/repos"

$centralRepo = "central-repo-name"

foreach ($repo in $repoList) {
    foreach ($file in $filesToSync) {
        $sourceFileUrl = "$baseUrl/$org/$centralRepo/contents/.github/$file"
        $destinationFileUrl = "$baseUrl/$org/$repo/contents/.github/$file"

        Write-Host "Fetching $file from $centralRepo to update in $repo..."
        $fileResponse = Invoke-RestMethod -Uri $sourceFileUrl -Method Get -Headers $headers
        $content = $fileResponse.content | Out-String | ConvertFrom-Base64String
        $sha = $fileResponse.sha

        $body = @{
            message = "Sync $file from $centralRepo"
            content = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($content))
            sha = $sha
        } | ConvertTo-Json

        Write-Host "Updating $file in $repo..."
        Invoke-RestMethod -Uri $destinationFileUrl -Method Put -Headers $headers -Body $body -ContentType "application/json"
        Write-Host "Successfully updated $file in $repo."
    }
}

Write-Host "Synchronization of files completed."
