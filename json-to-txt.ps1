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

# Create a formatted date string
$dateTime = Get-Date -Format "MM/dd/yyyy HH:mm:ss"
$buildVersion = "34.12421.1475.0"  # Replace with actual build version if needed

# Initialize output string
$output = @"
HPX Build Date: $dateTime
HPX Build Version: $buildVersion

| PACKAGE NAME (features) $("{ " * ($maxNameLength - 17)) | VERSION $("{ " * ($maxVersionLength - 7)) |
|$("-" * ($maxNameLength + 3))|$("-" * ($maxVersionLength + 2))|
"@

# Append features to output string
foreach ($key in $jsonContent.imports.Keys) {
    $name = $key
    $version = $jsonContent.imports.$key
    $output += "| $name$("{ " * ($maxNameLength - $name.Length + 1))| $version$("{ " * ($maxVersionLength - $version.Length + 1))|\n"
}

# Output file path
$outputFilePath = "path\to\your\outputfile.txt"
Set-Content -Path $outputFilePath -Value $output

Write-Host "Human-readable text file has been created at $outputFilePath"
