# Input Parameters
$DesktopCsprojPath = "C:\path\to\DesktopExtension.csproj"  # Update with your file path
$HpxCsprojPath = "C:\path\to\HP.HPX.csproj"               # Update with your file path
$NugetName = "HP.PenControl"                              # Update with your NuGet package name
$NewVersion = "1.0.3.50"                                  # Update with your new version

# Escape special characters in NugetName and NewVersion
$escapedNugetName = [regex]::Escape($NugetName)
$escapedNewVersion = [regex]::Escape($NewVersion)

# Function to Update a File and Test Regex
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

    # Debugging: Display matching lines
    Write-Host "Regex Pattern: $RegexPattern"
    $matches = Get-Content $FilePath | Select-String -Pattern $RegexPattern
    if ($matches) {
        Write-Host "Matched Lines:"
        $matches | ForEach-Object { Write-Host $_.Line }
    } else {
        Write-Host "No matches found for the regex in $FilePath" -ForegroundColor Yellow
        return
    }

    # Perform the replacement
    (Get-Content $FilePath) -replace $RegexPattern, $Replacement | Set-Content $FilePath -Encoding UTF8
    Write-Host "Successfully updated $FilePath" -ForegroundColor Green
}

# Regex for HP.HPX.csproj
$HpxRegex = "(<Content Include="".*?\\packages\\HP\.PenControl\\)[^\\]+"
$HpxReplacement = "`$1$escapedNewVersion"

# Regex for DesktopExtension.csproj
$DesktopRegex = "(<PackageReference Include=""HP\.PenControl"" Version="")[^""]+"
$DesktopReplacement = "`$1$escapedNewVersion"

# Update HP.HPX.csproj
Update-CsprojFile -FilePath $HpxCsprojPath -RegexPattern $HpxRegex -Replacement $HpxReplacement

# Update DesktopExtension.csproj
Update-CsprojFile -FilePath $DesktopCsprojPath -RegexPattern $DesktopRegex -Replacement $DesktopReplacement
