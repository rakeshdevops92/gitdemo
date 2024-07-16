# Function to remove .yarnrc file
function Remove-Yarnrc {
    $yarnrcPath = "C:\Users\$env:USERNAME\.yarnrc"
    if (Test-Path -Path $yarnrcPath) {
        Write-Output "Removing .yarnrc file at $yarnrcPath"
        Remove-Item -Path $yarnrcPath -Force
    } else {
        Write-Output ".yarnrc file does not exist at $yarnrcPath"
    }
}

# Function to check and update yarn version
function Check-And-Update-Yarn-Version {
    $requiredYarnVersion = "1.22.19"
    $currentYarnVersion = (yarn --version) -replace 'v', ''  # Remove 'v' prefix if it exists

    if ($currentYarnVersion -ne $requiredYarnVersion) {
        Write-Output "Uninstalling current Yarn version $currentYarnVersion"
        winget uninstall --id Yarn.Yarn -e

        Write-Output "Installing Yarn version $requiredYarnVersion"
        winget install --id Yarn.Yarn -e --version $requiredYarnVersion
    } else {
        Write-Output "Yarn is already at the required version: $requiredYarnVersion"
    }
}

# Main script execution
Remove-Yarnrc
Check-And-Update-Yarn-Version
