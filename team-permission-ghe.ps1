function Ensure-TeamPermission {
    param (
        [string]$repoName
    )
    
    $checkPermissionUrl = "$baseUrl/teams/$teamSlug/repos/$org/$repoName"
    
    try {
        $response = Invoke-RestMethod -Uri $checkPermissionUrl -Method GET -Headers $headers
        if ($response.permission -eq $null -or $response.permission -ne $role) {
            Write-Output "Team '$teamSlug' does not have the required permission for repository '$repoName'. Adding permission..."
            
            $addPermissionUrl = "$baseUrl/teams/$teamSlug/repos/$org/$repoName"
            $body = @{
                permission = $role
            } | ConvertTo-Json
            
            Invoke-RestMethod -Uri $addPermissionUrl -Method PUT -Headers $headers -Body $body
            Write-Output "Successfully added team '$teamSlug' to repository '$repoName' with role '$role'."
        } else {
            Write-Output "Team '$teamSlug' already has the required permission for repository '$repoName'."
        }
    } catch {
        Write-Error "Failed to check or add team permission for repository '$repoName'. Error: $_"
    }
}
