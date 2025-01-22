
# Define temporary directory for shorter path
$msixTempDirectory = "$(Build.SourcesDirectory)\msix_temp"
New-Item -ItemType Directory -Force -Path "$msixTempDirectory"

# Copy files to the temporary directory for handling long paths
Copy-Item -Path "$msixNewDirectory\*" -Destination "$msixTempDirectory" -Recurse -Force
Write-Host "Copied contents of $msixNewDirectory to $msixTempDirectory"

$envFiles = Get-ChildItem -Path $msixTempDirectory -Recurse -Filter "*.env"
