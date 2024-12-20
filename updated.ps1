# Update DesktopExtension.csproj References
(Get-Content $DesktopCsproj) -replace "($NugetName.*?, Version=)[0-9\.]+", "`$1$NewVersion" -replace "(HintPath.*?$NugetName\\.*?\\).*?(\")", "`$1$NewVersion`$2" | Set-Content $DesktopCsproj
Write-Host "Successfully updated $NugetName references in $DesktopCsproj"

# Update HP.HPX.csproj Content References
(Get-Content $HpxCsproj) -replace "(<Content Include=\".*?$NugetName\\.*?\\).*?(\")", "`$1$NewVersion`$2" | Set-Content $HpxCsproj
Write-Host "Successfully updated $NugetName content references in $HpxCsproj"
