Param(
 [string]$resourceGroup,
 [string]$VMName,
 [string]$method,
 [string]$UAMI 
)

$automationAccount = "testpuppetagent"

# Ensures you do not inherit an AzContext in your runbook
Disable-AzContextAutosave -Scope Process | Out-Null

# Connect using a Managed Service Identity
try {
        $AzureContext = (Connect-AzAccount -Identity).context
    }
catch{
        Write-Output "There is no system-assigned user identity. Aborting."; 
        exit
    }

# set and store context
$AzureContext = Set-AzContext -SubscriptionName $AzureContext.Subscription `
    -DefaultProfile $AzureContext

if ($method -eq "SA")
    {
        Write-Output "Using system-assigned managed identity"
    }
elseif ($method -eq "UA")
    {
        Write-Output "Using user-assigned managed identity"

        # Connects using the Managed Service Identity of the named user-assigned managed identity
        $identity = Get-AzUserAssignedIdentity -ResourceGroupName $resourceGroup `
            -Name $UAMI -DefaultProfile $AzureContext

        # validates assignment only, not perms
        if ((Get-AzAutomationAccount -ResourceGroupName $resourceGroup `
                -Name $automationAccount `
                -DefaultProfile $AzureContext).Identity.UserAssignedIdentities.Values.PrincipalId.Contains($identity.PrincipalId))
            {
                $AzureContext = (Connect-AzAccount -Identity -AccountId $identity.ClientId).context

                # set and store context
                $AzureContext = Set-AzContext -SubscriptionName $AzureContext.Subscription -DefaultProfile $AzureContext
            }
        else {
                Write-Output "Invalid or unassigned user-assigned managed identity"
                exit
            }
    }
else {
        Write-Output "Invalid method. Choose UA or SA."
        exit
     }

# Get current state of VM
$status = (Get-AzVM -ResourceGroupName $resourceGroup -Name $VMName `
    -Status -DefaultProfile $AzureContext).Statuses[1].Code

Write-Output "`r`n Beginning VM status: $status `r`n"

# Start or stop VM based on current state
# if($status -eq "Powerstate/deallocated")
#     {
#         Start-AzVM -Name $VMName -ResourceGroupName $resourceGroup -DefaultProfile $AzureContext
#     }
# elseif ($status -eq "Powerstate/running")
#     {
#         Stop-AzVM -Name $VMName -ResourceGroupName $resourceGroup -DefaultProfile $AzureContext -Force
#     }

$myDownloadUrl = "https://raw.githubusercontent.com/rakeshdevops92/gitdemo/main/puppetagent.ps1"
Invoke-WebRequest $myDownloadUrl -OutFile ScriptToRun.ps1 
Invoke-AzVMRunCommand -ResourceGroupName $resourceGroup -Name $VMName -CommandId 'RunPowerShellScript' -ScriptPath ScriptToRun.ps1
Remove-Item -Path ScriptToRun.ps1

Write-Output "`r`n Ending VM status: success `r`n `r`n"

Write-Output "Account ID of current context: " $AzureContext.Account.Id
