try {
    New-Item -ItemType Directory -Force -Path $msixNewDirectory
    Write-Host "Directory created successfully: $msixNewDirectory"
}
catch {
    Write-Host "Initial attempt failed. Trying with '\\' prefix."
    $msixNewDirectory = "\\$msixNewDirectory"

    try {
        New-Item -ItemType Directory -Force -Path $msixNewDirectory
        Write-Host "Directory created successfully with '\\' prefix: $msixNewDirectory"
    }
    catch {
        Write-Error "Failed to create directory even with '\\' prefix: $($_.Exception.Message)"
        Out-File -FilePath "error_log.txt" -Append -InputObject $_.Exception.Message
    }
}
