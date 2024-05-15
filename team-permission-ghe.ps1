# Variables
$orgName = "HPI"
$teamSlug = "hpx-devops"
$githubToken = "YOUR_GITHUB_PAT"
$role = "push"  # Role can be one of: push (write), pull (read), admin

# Headers
$headers = @{
    Authorization = "token $githubToken"
    Accept        = "application/vnd.github.v3+json"
}

# Get all repositories in the organization
$reposUrl = "https://api.github.com/orgs/$orgName/repos?per_page=100"
$repos = Invoke-RestMethod -Uri $reposUrl -Headers $headers

foreach ($repo in $repos) {
    $repoName = $repo.name
    $addTeamUrl = "https://api.github.com/orgs/$orgName/teams/$teamSlug/repos/$orgName/$repoName"
    
    $body = @{
        permission = $role
    } | ConvertTo-Json
    
    Write-Output "Adding team '$teamSlug' to repository '$repoName' with role '$role'..."
    
    try {
        Invoke-RestMethod -Uri $addTeamUrl -Method PUT -Headers $headers -Body $body
        Write-Output "Successfully added team '$teamSlug' to repository '$repoName'."
    } catch {
        Write-Output "Failed to add team '$teamSlug' to repository '$repoName'. Error: $_"
    }
}

Write-Output "Team added to all repositories."
