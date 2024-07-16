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
    $currentYarnVersion = yarn --version

    if ($currentYarnVersion -ne $requiredYarnVersion) {
        Write-Output "Updating Yarn to version $requiredYarnVersion"
        npm install -g yarn@$requiredYarnVersion
    } else {
        Write-Output "Yarn is already at the required version: $requiredYarnVersion"
    }
}

# Main script execution
Remove-Yarnrc
Check-And-Update-Yarn-Version
