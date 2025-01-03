try {
    $msixNewDirectory = Join-Path -Path $msixBundleNewDirectory -ChildPath ($msixName -replace '\.msix$', '')

    if ($msixNewDirectory -match '^\\\\') {
        $msixNewDirectory = "\\$msixNewDirectory"
    }

    if (-not ([System.IO.Path]::IsPathRooted($msixNewDirectory) -and
              -not ($msixNewDirectory -match '[<>:"|?*]'))) {
        throw "Invalid path detected: $msixNewDirectory"
    }

    New-Item -ItemType Directory -Force -Path $msixNewDirectory
    Write-Host "Directory created successfully: $msixNewDirectory"
}
catch {
    Write-Error "Failed to create directory: $($_.Exception.Message)"
    Out-File -FilePath "error_log.txt" -Append -InputObject $_.Exception.Message
}
