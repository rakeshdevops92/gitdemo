Install-Module -Name NewAzDoServiceConnection -Scope CurrentUser -Force
Import-Module -Name NewAzDoServiceConnection
$Parameters = @{
    AzServicePrincipalName = "unique sp in your tenent"
    AzDoConnectionName     = "your service con"
    AzSubscriptionName     = "your subscription name"
    AzResourceGroupScope   = "your resource group name"
    AzRole                 = "contributor"
    AzDoOrganizationName   = "yourOrg"
    AzDoProjectName        = "yourProj"
    AzDoUserName           = "your@email.com"
    AzDoToken              = "your-pat"
}

New-AzDoServiceConnection @Parameters
