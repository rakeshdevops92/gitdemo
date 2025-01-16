# Input Parameters
$DesktopCsprojPath = "C:\Path\To\DesktopExtension.csproj"  # Replace with your file path
$HpxCsprojPath = "C:\Path\To\HP.HPX.csproj"               # Replace with your file path
$NugetName = "HP.PenControl"                              # NuGet package name
$NewVersion = "1.0.3.50"                                  # New version

# Escape special characters in NuGet name for regex
$escapedNugetName = [regex]::Escape($NugetName)

# Function to update .csproj files
function Update-CsprojFile {
    param (
        [string]$FilePath,
        [string]$RegexPattern,
        [string]$Replacement
    )

    Write-Host "Processing File: $FilePath"

    # Validate the file exists
    if (!(Test-Path $FilePath)) {
        Write-Host "Error: File not found at $FilePath" -ForegroundColor Red
        return
    }

    # Read the file content
    $fileContent = Get-Content $FilePath

    # Check for matches and update if found
    $matches = $fileContent | Select-String -Pattern $RegexPattern
    if ($matches) {
        Write-Host "Match found. Updating..."
        $updatedContent = $fileContent -replace $RegexPattern, $Replacement
        Set-Content $FilePath -Value $updatedContent -Encoding UTF8
        Write-Host "File updated successfully: $FilePath" -ForegroundColor Green
    } else {
        Write-Host "No matches found in $FilePath for pattern: $RegexPattern" -ForegroundColor Yellow
    }
}

# Regex patterns and replacements

# For HP.HPX.csproj
$HpxRegex = '<Content Include="\.\.\\packages\\' + $escapedNugetName + '\\[^\\]+\\(.*)"'
$HpxReplacement = '<Content Include="..\packages\' + $NugetName + '\' + $NewVersion + '\$1"'

# For DesktopExtension.csproj
$DesktopRegex = '<PackageReference Include="' + $escapedNugetName + '" Version="[^"]+"'
$DesktopReplacement = '<PackageReference Include="' + $NugetName + '" Version="' + $NewVersion + '"'

# Update the files
Update-CsprojFile -FilePath $HpxCsprojPath -RegexPattern $HpxRegex -Replacement $HpxReplacement
Update-CsprojFile -FilePath $DesktopCsprojPath -RegexPattern $DesktopRegex -Replacement $DesktopReplacement