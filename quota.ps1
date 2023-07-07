param (
    [Parameter(Mandatory = $true)]
    [string] $Region,

    [Parameter(Mandatory = $true)]
    [int] $Threshold
)

# Ensures you do not inherit an AzContext in your runbook
Disable-AzContextAutosave -Scope Process

# Connect to Azure with system-assigned managed identity
$AzureContext = (Connect-AzAccount -Identity).context

# Set and store context
$AzureContext = Set-AzContext -SubscriptionName $AzureContext.Subscription -DefaultProfile $AzureContext

# Log the start of the Runbook
Write-Output "Starting VM Quota Limit Check Runbook..."

# Get the VM usage data for the specified region
$vmusage = Get-AzVMUsage -Location $Region | Where-Object { $_.Name.LocalizedValue -eq "Virtual Machines" } | Select-Object @{Name = 'VMName'; Expression = {$_.Name.LocalizedValue}}, CurrentValue, Limit

# Calculate the availability as the difference between the limit and current value
$availability = $vmUsage.Limit - $vmUsage.CurrentValue

# Log the current, limit, and availability values
Write-Output "Current VMs: $($vmUsage.CurrentValue)"
Write-Output "Limit VMs: $($vmUsage.Limit)"
Write-Output "Availability: $availability"

# Check if the availability is below the threshold
if ($availability -lt $Threshold) {
    Write-Output "VM availability in region $Region is below the threshold of $Threshold."

    # Create a support ticket with Microsoft
    $ticketParams = @{
        Name = "VM Quota Limit Alert"
        Severity = "minimal"
        ProblemClassificationId = "/providers/Microsoft.Support/services/{billing_service_guid}/problemClassifications/{problemClassification_guid}"  # Replace with the appropriate Problem Classification ID
        CustomerFirstName = "Rakesh"
        CustomerLastName = "Chanamala"
        PreferredContactMethod = "Email"
        CustomerPrimaryEmailAddress = "rakesh.chanamala1@carrier.com"
        CustomerPreferredTimeZone = "UTC"
        CustomerCountry = "United States"
        CustomerPreferredSupportLanguage = "English"
        Title = "VM Quota Limit Alert"
        Description = "The VM availability in region $Region is less. Please increase the quota."
    }
    Write-Output "Creating support ticket with Microsoft..."
    New-AzSupportTicket @ticketParams

    Write-Output "Support ticket created with Microsoft."
} else {
    Write-Output "VM availability in region $Region is within the threshold."
}

# Log the end of the Runbook
Write-Output "VM Quota Limit Check Runbook completed."
