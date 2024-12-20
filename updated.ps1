targetType: 'inline'
workingDirectory: $(Build.Repository.LocalPath)/$(nugetPath)/${{ parameters.nugetName }}
script: |
  $AssemblyFile = "$(Build.Repository.LocalPath)\$(nugetPath)\${{ parameters.nugetName }}\Properties\AssemblyInfo.cs"
  $DesktopCsproj = "$(Build.Repository.LocalPath)\apps\HPX\windows\DesktopExtension\DesktopExtension.csproj"
  $HpxCsproj = "$(Build.Repository.LocalPath)\apps\HPX\windows\HP.HPX\HP.HPX.csproj"
  $NewVersion = "${{ parameters.PackageVersion }}"
  $NugetName = "${{ parameters.nugetName }}"

  $FilesToCheck = @($AssemblyFile, $DesktopCsproj, $HpxCsproj)

  foreach ($file in $FilesToCheck) {
      if (-Not (Test-Path $file)) {
          Write-Host "Error: File not found: $file"
          exit 1
      }
  }

  (Get-Content $AssemblyFile) -replace '\[assembly: AssemblyVersion\(".*"\)\]', "[assembly: AssemblyVersion(`"$NewVersion`")]" | Set-Content $AssemblyFile
  (Get-Content $AssemblyFile) -replace '\[assembly: AssemblyFileVersion\(".*"\)\]', "[assembly: AssemblyFileVersion(`"$NewVersion`")]" | Set-Content $AssemblyFile
  Write-Host "Successfully updated AssemblyVersion and AssemblyFileVersion in $AssemblyFile"

  (Get-Content $DesktopCsproj) -replace "($NugetName.*?, Version=)[0-9\.]+", "`$1$NewVersion" `
                              -replace "(HintPath.*?$NugetName\\.*?\\).*?(\")", "`$1$NewVersion`$2" | Set-Content $DesktopCsproj
  Write-Host "Successfully updated $NugetName references in $DesktopCsproj"

  (Get-Content $HpxCsproj) -replace "(<Content Include=\".*?$NugetName\\.*?\\).*?(\")", "`$1$NewVersion`$2" | Set-Content $HpxCsproj
  Write-Host "Successfully updated $NugetName content references in $HpxCsproj"

  Write-Host "Contents of AssemblyInfo.cs post update:"
  Get-Content $AssemblyFile | ForEach-Object { Write-Host $_ }

  Write-Host "Contents of DesktopExtension.csproj post update:"
  Get-Content $DesktopCsproj | ForEach-Object { Write-Host $_ }

  Write-Host "Contents of HP.HPX.csproj post update:"
  Get-Content $HpxCsproj | ForEach-Object { Write-Host $_ }
