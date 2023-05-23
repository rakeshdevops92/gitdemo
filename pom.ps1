# Specify the path to the pom.xml file
$pomPath = "path\to\pom.xml"

# Load the pom.xml content
$xml = [xml](Get-Content -Path $pomPath)

# Get the value of the <packaging> tag
$packaging = $xml.project.packaging

# Output the value of the <packaging> tag
Write-Output "Packaging: $packaging"
