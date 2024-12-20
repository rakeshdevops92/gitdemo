- task: PowerShell@2
  displayName: "Set NuGet Details Dynamically"
  inputs:
    targetType: inline
    script: |
      # NuGet mappings
      $nugetMappings = @{
          "HP.PenControl"             = @{ Path="nugets/HP.PenControl"; Solution="HP.PenControl.sln"; Assembly="Properties/AssemblyInfo.cs" }
          "HP.AccessoryControl"       = @{ Path="nugets/HP.AccessoryControl"; Solution="HP.AccessoryControl.sln"; Assembly="Properties/AssemblyInfo.cs" }
          "HP.AppFramework.AuthService" = @{ Path="nugets/HP.AppFramework.AuthService"; Solution="HP.AppFramework.AuthService.sln"; Assembly="Properties/AssemblyInfo.cs" }
          "HP.AppFramework.LoggingDE" = @{ Path="nugets/HP.AppFramework.LoggingDE"; Solution="HP.AppFramework.LoggingDE.sln"; Assembly="Properties/AssemblyInfo.cs" }
          "HP.AppFramework.Win32DE"   = @{ Path="nugets/HP.AppFramework.Win32DE"; Solution="HP.AppFramework.Win32DE.sln"; Assembly="Properties/AssemblyInfo.cs" }
          "HP.AudioControl"           = @{ Path="nugets/HP.AudioControl"; Solution="HP.AudioControl.sln"; Assembly="Properties/AssemblyInfo.cs" }
          "HP.Calculator"             = @{ Path="nugets/HP.Calculator"; Solution="HP.Calculator.sln"; Assembly="Properties/AssemblyInfo.cs" }
          "HP.CameraStatus"           = @{ Path="nugets/HP.CameraStatus"; Solution="HP.CameraStatus.sln"; Assembly="Properties/AssemblyInfo.cs" }
      }

      # Retrieve selected NuGet details
      $selectedNuget = "${{ parameters.nugetName }}"
      $details = $nugetMappings[$selectedNuget]

      # Debugging output
      if (-not $details) {
          Write-Host "##vso[task.logissue type=error]Selected NuGet '$selectedNuget' not found in mappings."
          exit 1
      }

      Write-Host "Selected NuGet: $selectedNuget"
      Write-Host "Path: $($details.Path)"
      Write-Host "Solution File: $($details.Solution)"
      Write-Host "Assembly File: $($details.Assembly)"

      # Set pipeline variables
      Write-Host "##vso[task.setvariable variable=nugetPath]$($details.Path)"
      Write-Host "##vso[task.setvariable variable=solutionFile]$($details.Solution)"
      Write-Host "##vso[task.setvariable variable=assemblyFile]$($details.Assembly)"
