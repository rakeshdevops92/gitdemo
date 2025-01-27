$filePath = "path\to\your\file.xml"

$newVersion = "1.0.4.60"
$newAssemblyVersion = "1.0.4.60"
$newFileVersion = "1.0.4.60"

[xml]$xml = Get-Content -Path $filePath

$hpPenControlGroup = $xml.Project.PropertyGroup | Where-Object { $_.PackageId -eq "HP.PenControl" }

if ($hpPenControlGroup) {
    $hpPenControlGroup.Version = $newVersion
    $hpPenControlGroup.AssemblyVersion = $newAssemblyVersion
    $hpPenControlGroup.FileVersion = $newFileVersion

    $xml.Save($filePath)

    Write-Host "Version, AssemblyVersion, and FileVersion updated successfully for HP.PenControl."
} else {
    Write-Host "HP.PenControl PropertyGroup not found in the XML file."
}
