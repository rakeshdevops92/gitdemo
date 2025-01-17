# Input Parameters
$inputVersion = "2.0.2.33" # Update this to the desired version
$filePaths = @("C:\Work\Support\Subhash\gitdemo\assemblyversion\HP.HPX.csproj", "C:\Work\Support\Subhash\gitdemo\assemblyversion\DesktopExtension.csproj") # Update with the paths to your .csproj files

# Function to update version in the file
function Update-VersionInCsproj {
    param (
        [string]$filePath,
        [string]$version
    )
    
    # Read the file content
    $content = Get-Content $filePath
    
    # Update PackageReference lines
    $content = $content -replace '(?<=<PackageReference Include="HP.PenControl" Version=")[^"]+', $version
    $content = $content -replace '(?<=<Content Include="\.\.\\packages\\HP\.PenControl\\)[^\\]+', $version
    
    # Write the updated content back to the file
    Set-Content -Path $filePath -Value $content -Encoding UTF8
    
    Write-Host "Updated version to $version in $filePath"
}

# Iterate over the files and update the version
foreach ($file in $filePaths) {
    Update-VersionInCsproj -filePath $file -version $inputVersion
}
