$ResourceGroupName = "<YourResourceGroupName>"
$WorkspaceResourceId = "<LogAnalyticsWorkspaceResourceId>"
$DatadogEndpoint = "<DatadogEndpoint>"
$SendTo = "LogAnalytics"

if ($ResourceGroupName) {
    $apps = Get-AzWebApp -ResourceGroupName $ResourceGroupName
} else {
    $apps = Get-AzWebApp
}

foreach ($app in $apps) {
    Write-Host "Processing App: $($app.Name)"
    $diagSettings = Get-AzDiagnosticSetting -ResourceId $app.Id -ErrorAction SilentlyContinue

    if ($diagSettings) {
        Write-Host "Diagnostic settings are already enabled for $($app.Name)." -ForegroundColor Green
    } else {
        Write-Host "Diagnostic settings are not enabled for $($app.Name). Enabling now..." -ForegroundColor Yellow

        if ($SendTo -eq "LogAnalytics") {
            Set-AzDiagnosticSetting -ResourceId $app.Id `
                                    -WorkspaceId $WorkspaceResourceId `
                                    -Name "EnableDiagnostics" `
                                    -Category @("AppServiceHTTPLogs", "AppServiceConsoleLogs", "AppServiceAppLogs") `
                                    -Enabled $true
            Write-Host "Diagnostic settings enabled for Log Analytics Workspace." -ForegroundColor Green
        } elseif ($SendTo -eq "Datadog") {
            $datadogSettings = @{
                "logs" = @{
                    "enabled" = $true
                }
                "metrics" = @{
                    "enabled" = $true
                }
            }
            Set-AzDiagnosticSetting -ResourceId $app.Id `
                                    -Name "EnableDiagnostics" `
                                    -LogsToEventHub `
                                    -EventHubAuthorizationRuleId $DatadogEndpoint `
                                    -Enabled $true
            Write-Host "Diagnostic settings enabled for Datadog." -ForegroundColor Green
        } else {
            Write-Host "Invalid logging destination specified. Please use 'LogAnalytics' or 'Datadog'." -ForegroundColor Red
        }
    }
}

Write-Host "Processing complete!"
