param(
    [Parameter(Mandatory=$true)]
    [ValidateSet('major','minor','patch')]
    [string]$type
)

# Load the package.json file
$jsonPath = "path\to\package.json"
$json = Get-Content $jsonPath | ConvertFrom-Json

# Extract the current version and split into major, minor, and patch
$versionParts = $json.version -split '\.'

# Increment the version based on the input type
switch ($type) {
    'major' {
        $versionParts[0] = [int]$versionParts[0] + 1
        $versionParts[1] = 0
        $versionParts[2] = 0
    }
    'minor' {
        $versionParts[1] = [int]$versionParts[1] + 1
        $versionParts[2] = 0
    }
    'patch' {
        $versionParts[2] = [int]$versionParts[2] + 1
    }
}

# Reconstruct the version string
$newVersion = "$($versionParts[0]).$($versionParts[1]).$($versionParts[2])"

# Update the version in the JSON object
$json.version = $newVersion

# Convert the JSON object back to a string
$jsonString = $json | ConvertTo-Json -Depth 100

# Write the updated JSON back to the file
$jsonString | Set-Content $jsonPath

# Output the new version
Write-Output "Updated version to $newVersion"
