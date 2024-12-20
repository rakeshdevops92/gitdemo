
  # Define paths dynamically based on selected nugetName and packageVersion passed as environment variables
  $NugetName = "${env:NugetName}"
  $NewVersion = "${env:PackageVersion}"

  # Paths
  $AssemblyFile = "$(Build.Repository.LocalPath)\$(nugetPath)\$NugetName\Properties\AssemblyInfo.cs"
  $DesktopCsproj = "$(Build.Repository.LocalPath)\apps\HPX\windows\DesktopExtension\DesktopExtension.csproj"
  $HpxCsproj = "$(Build.Repository.LocalPath)\apps\HPX\windows\HP.HPX\HP.HPX.csproj"

  # Echo all variables for debugging
  Write-Host "### Debugging Variables ###"
  Write-Host "Build.Repository.LocalPath: $(Build.Repository.LocalPath)"
  Write-Host "nugetPath: $(nugetPath)"
  Write-Host "NugetName: $NugetName"
  Write-Host "PackageVersion: $NewVersion"
  Write-Host "AssemblyFile Path: $AssemblyFile"
  Write-Host "DesktopCsproj Path: $DesktopCsproj"
  Write-Host "HpxCsproj Path: $HpxCsproj"
  Write-Host "############################"

  # Files to check
  $FilesToCheck = @($AssemblyFile, $DesktopCsproj, $HpxCsproj)

  foreach ($file in $FilesToCheck) {
      if (-Not (Test-Path $file)) {
          Write-Host "Error: File not found: $file"
          exit 1
      }
  }

  # Update Assembly Version and File Version
  (Get-Content $AssemblyFile) -replace '\[assembly: AssemblyVersion\(".*?"\)\]', "[assembly: AssemblyVersion(`"$NewVersion`")]" | Set-Content $AssemblyFile
  (Get-Content $AssemblyFile) -replace '\[assembly: AssemblyFileVersion\(".*?"\)\]', "[assembly: AssemblyFileVersion(`"$NewVersion`")]" | Set-Content $AssemblyFile
  Write-Host "Successfully updated AssemblyVersion and AssemblyFileVersion in $AssemblyFile"

  # Update DesktopExtension.csproj References
  (Get-Content $DesktopCsproj) `
      -replace "($NugetName.*?, Version=)[0-9\.]+", "$1$NewVersion" `
      -replace "(HintPath.*?$NugetName\\.*?\\).*?(\")", "$1$NewVersion$2" `
      | Set-Content $DesktopCsproj
  Write-Host "Successfully updated $NugetName references in $DesktopCsproj"

  # Update HP.HPX.csproj Content References
  (Get-Content $HpxCsproj) `
      -replace "(<Content Include=\".*?$NugetName\\.*?\\).*?(\")", "$1$NewVersion$2" `
      | Set-Content $HpxCsproj
  Write-Host "Successfully updated $NugetName content references in $HpxCsproj"

  # Log file contents post update
  Write-Host "Contents of AssemblyInfo.cs post update:"
  Get-Content $AssemblyFile | ForEach-Object { Write-Host $_ }

  Write-Host "Contents of DesktopExtension.csproj post update:"
  Get-Content $DesktopCsproj | ForEach-Object { Write-Host $_ }

  Write-Host "Contents of HP.HPX.csproj post update:"
  Get-Content $HpxCsproj | ForEach-Object { Write-Host $_ }
env:
  NugetName: ${{ parameters.nugetName }}
  PackageVersion: ${{ parameters.PackageVersion }}
