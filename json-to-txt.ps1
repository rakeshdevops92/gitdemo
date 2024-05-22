# Read JSON file and parse it
$jsonFilePath = "path\to\your\jsonfile.json"
$jsonContent = Get-Content -Raw -Path $jsonFilePath | ConvertFrom-Json

# Initialize variables for storing max lengths
$maxNameLength = 0
$maxVersionLength = 0

# Determine max lengths for formatting
foreach ($key in $jsonContent.imports.Keys) {
    $nameLength = $key.Length
    $versionLength = $jsonContent.imports.$key.Length

    if ($nameLength -gt $maxNameLength) {
        $maxNameLength = $nameLength
    }

    if ($versionLength -gt $maxVersionLength) {
        $maxVersionLength = $versionLength
    }
}

# Ensure that the padding values are not negative
$namePadding = [math]::Max($maxNameLength - 17, 0)
$versionPadding = [math]::Max($maxVersionLength - 7, 0)

# Create a formatted date string
$dateTime = Get-Date -Format "MM/dd/yyyy HH:mm:ss"
$buildVersion = "34.12421.1475.0"  # Replace with actual build version if needed

# Initialize output string
$output = "HPX Build Date: $dateTime`n"
$output += "HPX Build Version: $buildVersion`n`n"
$output += "| PACKAGE NAME (features) " + " " * $namePadding + "| VERSION " + " " * $versionPadding + "|`n"
$output += "|" + "-" * ($maxNameLength + 1) + "|" + "-" * ($maxVersionLength + 1) + "|`n"

# Append features to output string
foreach ($key in $jsonContent.imports.Keys) {
    $name = $key
    $version = $jsonContent.imports.$key
    $output += "| $name" + " " * ([math]::Max($maxNameLength - $name.Length + 1, 0)) + "| $version" + " " * ([math]::Max($maxVersionLength - $version.Length + 1, 0)) + "|`n"
}

# Output file path
$outputFilePath = "path\to\your\outputfile.txt"
Set-Content -Path $outputFilePath -Value $output

Write-Host "Human-readable text file has been created at $outputFilePath"
