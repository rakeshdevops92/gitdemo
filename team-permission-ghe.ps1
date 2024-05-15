
function Ensure-TeamPermission {
    param (
        [string]$repoName
    )
    
    $checkPermissionUrl = "https://api.github.com/orgs/$org/teams/$teamSlug/repos/$org/$repoName"
    
    try {
        $response = Invoke-RestMethod -Uri $checkPermissionUrl -Method GET -Headers $headers
        Write-Output "Team '$teamSlug' already has permission for repository '$repoName'."
    } catch {
        if ($_.Exception.Response.StatusCode -eq [System.Net.HttpStatusCode]::NotFound) {
            Write-Output "Team '$teamSlug' does not have permission for repository '$repoName'. Adding permission..."
            
            $addPermissionUrl = "https://api.github.com/orgs/$org/teams/$teamSlug/repos/$org/$repoName"
            $body = @{
                permission = $role
            } | ConvertTo-Json
            
            Invoke-RestMethod -Uri $addPermissionUrl -Method PUT -Headers $headers -Body $body
            Write-Output "Successfully added team '$teamSlug' to repository '$repoName' with role '$role'."
        } else {
            Write-Error "Failed to check or add team permission for repository '$repoName'. Error: $_"
        }
    }
}
