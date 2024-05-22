# Read JSON file and parse it
$jsonFilePath = ".\importmap.json"
$jsonContent = Get-Content -Raw -Path $jsonFilePath | ConvertFrom-Json

# Verify the structure of the JSON
if (-not $jsonContent.imports) {
    Write-Host "The 'imports' property is not found in the JSON content."
    exit 1
}

# Initialize variables for storing max lengths
$maxNameLength = 0
$maxVersionLength = 0

# Determine max lengths for formatting
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

# Ensure the lengths are at least as long as the header titles
$maxNameLength = [math]::Max($maxNameLength, 20)
$maxVersionLength = [math]::Max($maxVersionLength, 7)

# Create a formatted date string
$dateTime = Get-Date -Format "MM/dd/yyyy HH:mm:ss"
$buildVersion = "34.12421.1475.0"  # Replace with actual build version if needed

# Initialize output string
$output = "HPX Build Date: $dateTime`n"
$output += "HPX Build Version: $buildVersion`n`n"
$output += "| PACKAGE NAME (features) " + " " * ($maxNameLength - 20) + "| VERSION " + " " * ($maxVersionLength - 7) + "|`n"
$output += "|" + "-" * ($maxNameLength + 2) + "|" + "-" * ($maxVersionLength + 8) + "|`n"

# Append features to output string
foreach ($key in $jsonContent.imports.PSObject.Properties.Name) {
    $name = $key
    $version = $jsonContent.imports.$key
    $output += "| " + $name + " " * ($maxNameLength - $name.Length + 1) + "| " + $version + " " * ($maxVersionLength - $version.Length + 1) + "|`n"
}

# Output file path
$outputFilePath = ".\outputfile.txt"
Set-Content -Path $outputFilePath -Value $output -Force

Write-Host "Human-readable text file has been created at $outputFilePath"
