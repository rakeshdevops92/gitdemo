param (
    [string]$jsonFilePath,
    [string]$outputFilePath,
    [string]$buildVersion
)

$jsonContent = Get-Content -Raw -Path $jsonFilePath | ConvertFrom-Json

# Verifying the structure of the JSON
if (-not $jsonContent.imports) {
    Write-Host "The 'imports' property is not found in the JSON content."
    exit 1
}

$maxNameLength = 0
$maxVersionLength = 0

foreach ($key in $jsonContent.imports.PSObject.Properties.Name) {
    $nameLength = $key.Length
    $versionLength = $jsonContent.imports.$key.Length

    if ($nameLength -gt $maxNameLength) {
        $maxNameLength = $nameLength
    }

    if ($versionLength -gt $maxVersionLength) {
        $maxVersionLength = $versionLength
    }
}

$maxNameLength = [math]::Max($maxNameLength, 20)
$maxVersionLength = [math]::Max($maxVersionLength, 7)

$dateTime = Get-Date -Format "MM/dd/yyyy HH:mm:ss"

$output = "HPX Build Date: $dateTime`n"
$output += "HPX Build Version: $buildVersion`n`n"
$output += "| PACKAGE NAME (features) " + " " * ($maxNameLength - 20) + "| VERSION " + " " * ($maxVersionLength - 7) + "|`n"
$output += "|" + "-" * ($maxNameLength + 2) + "|" + "-" * ($maxVersionLength + 8) + "|`n"

foreach ($key in $jsonContent.imports.PSObject.Properties.Name) {
    $name = $key
    $version = $jsonContent.imports.$key
    $output += "| " + $name + " " * ($maxNameLength - $name.Length + 1) + "| " + $version + " " * ($maxVersionLength - $version.Length + 1) + "|`n"
}

Set-Content -Path $outputFilePath -Value $output -Force
Write-Host "Human-readable text file has been created at $outputFilePath"
