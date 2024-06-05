param (
    [string]$jsonFilePath,
    [string]$outputFilePath,
    [string]$buildVersion
)

function Get-VersionFromUrl {
    param (
        [string]$url
    )
    if ($url -match "/(\d+\.\d+\.\d+(\.\d+)?)/[^/]+$") {
        return $matches[1]
    } else {
        return ""
    }
}

$jsonContent = Get-Content -Raw -Path $jsonFilePath | ConvertFrom-Json

if (-not $jsonContent.imports) {
    Write-Host "The 'imports' property is not found in the JSON content."
    exit 1
}

$maxNameLength = 0
$maxVersionLength = 0
$maxUrlLength = 0

foreach ($key in $jsonContent.imports.PSObject.Properties.Name) {
    $nameLength = $key.Length
    $url = $jsonContent.imports.$key
    $version = Get-VersionFromUrl -url $url
    $versionLength = $version.Length
    $urlLength = $url.Length

    if ($nameLength -gt $maxNameLength) {
        $maxNameLength = $nameLength
    }

    if ($versionLength -gt $maxVersionLength) {
        $maxVersionLength = $versionLength
    }

    if ($urlLength -gt $maxUrlLength) {
        $maxUrlLength = $urlLength
    }
}

$maxNameLength = [math]::Max($maxNameLength, 30)
$maxVersionLength = [math]::Max($maxVersionLength, 10)
$maxUrlLength = [math]::Max($maxUrlLength, 50)

$dateTime = Get-Date -Format "MM/dd/yyyy HH:mm:ss"

$output = "HPX Build Date: $dateTime`n"
$output += "HPX Build Version: $buildVersion`n`n"
$output += "| PACKAGE NAME (features)" + " " * ($maxNameLength - 23) + " | VERSION" + " " * ($maxVersionLength - 7) + " | URL" + " " * ($maxUrlLength - 3) + " |`n"
$output += "|" + "-" * ($maxNameLength + 2) + "|" + "-" * ($maxVersionLength + 2) + "|" + "-" * ($maxUrlLength + 2) + "|`n"

foreach ($key in $jsonContent.imports.PSObject.Properties.Name) {
    $name = $key
    $url = $jsonContent.imports.$key
    $version = Get-VersionFromUrl -url $url
    $output += "| " + $name + " " * ($maxNameLength - $name.Length) + " | " + $version + " " * ($maxVersionLength - $version.Length) + " | " + $url + " " * ($maxUrlLength - $url.Length) + " |`n"
}

Set-Content -Path $outputFilePath -Value $output -Force

Write-Host "Text file has been created at $outputFilePath"
