$assemblyFile = "$(Build.Repository.LocalPath)\nugets\HP.PenControl\HP.PenControl\Properties\AssemblyInfo.cs"
$desktopCsproj = "$(Build.Repository.LocalPath)\apps\HPX\windows\DesktopExtension\DesktopExtension.csproj"
$packagesConfig = "$(Build.Repository.LocalPath)\apps\HPX\windows\DesktopExtension\packages.config"
$hpxCsproj = "$(Build.Repository.LocalPath)\apps\HPX\windows\HP.HPX.csproj"
$newVersion = "$(PackageVersion)"

$filesToCheck = @($assemblyFile, $desktopCsproj, $packagesConfig, $hpxCsproj)
foreach ($file in $filesToCheck) {
    if (-Not (Test-Path $file)) {
        Write-Host "Error: File not found: $file"
        exit 1
    }
}

(Get-Content $assemblyFile) -replace '\[assembly: AssemblyVersion\(".*?"\)\]', "[assembly: AssemblyVersion(`"$newVersion`")]" | Set-Content $assemblyFile
(Get-Content $assemblyFile) -replace '\[assembly: AssemblyFileVersion\(".*?"\)\]', "[assembly: AssemblyFileVersion(`"$newVersion`")]" | Set-Content $assemblyFile
Write-Host "Successfully updated AssemblyVersion and AssemblyFileVersion in $assemblyFile"

(Get-Content $desktopCsproj) -replace '(HP\.PenControl.*?, Version=)[0-9.]+', "`$1$newVersion" `
                             -replace '(<HintPath>.*?HP\.PenControl\\)[^\\]+', "`$1$newVersion" | Set-Content $desktopCsproj
Write-Host "Successfully updated HP.PenControl references in $desktopCsproj"

(Get-Content $packagesConfig) -replace '(<package id="HP\.PenControl".*?version=")[^"]+', "`$1$newVersion" | Set-Content $packagesConfig
Write-Host "Successfully updated HP.PenControl version in $packagesConfig"

(Get-Content $hpxCsproj) -replace '(<Content Include=".*?HP\.PenControl\\)[^\\]+', "`$1$newVersion" | Set-Content $hpxCsproj
Write-Host "Successfully updated HP.PenControl content references in $hpxCsproj"

Write-Host "Contents of AssemblyInfo.cs post update:"
Get-Content $assemblyFile | ForEach-Object { Write-Host $_ }

Write-Host "Contents of DesktopExtension.csproj post update:"
Get-Content $desktopCsproj | ForEach-Object { Write-Host $_ }

Write-Host "Contents of packages.config post update:"
Get-Content $packagesConfig | ForEach-Object { Write-Host $_ }

Write-Host "Contents of HP.HPX.csproj post update:"
Get-Content $hpxCsproj | ForEach-Object { Write-Host $_ }
