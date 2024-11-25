# Azure Diagnostic Settings Configuration Script

## Overview

This PowerShell script checks diagnostic settings for all Azure App Services and Function Apps in a specified resource group (or all resource groups in the subscription). If diagnostic settings are not enabled, the script configures them to send logs to either:

- **Log Analytics Workspace**
- **Datadog**

The logging destination can be configured based on your requirement.

---

## Features

- Checks the current status of diagnostic settings for Azure App Services and Function Apps.
- Automatically enables diagnostic settings if not already configured.
- Sends logs to:
  - **Azure Log Analytics Workspace**
  - **Datadog** (via Event Hub endpoint)
- Processes all or specific resource groups.

---

## Prerequisites

1. **Azure PowerShell Module**: Ensure the Azure PowerShell module is installed:
   ```powershell
   Install-Module -Name Az -AllowClobber -Scope CurrentUser

---

### Azure Authentication

Log in to your Azure account using the following command:

   ```powershell
    Connect-AzAccount

---

### Required Permissions

Ensure that you have sufficient permissions to manage App Services and configure diagnostic settings in your Azure subscription. This includes:

- Contributor or Owner permissions for the target subscription or resource group.
- Ability to read and write diagnostic settings for Azure resources.

## Script Parameters

Before running the script, update the following variables in the script file:

| Parameter             | Description                                                                                  |
|-----------------------|----------------------------------------------------------------------------------------------|
| `$ResourceGroupName`  | The Azure Resource Group name. Leave it empty (`""`) to process all resource groups.         |
| `$WorkspaceResourceId`| Resource ID of the Log Analytics Workspace where logs will be sent.                          |
| `$DatadogEndpoint`    | Datadog Event Hub endpoint where logs will be sent.                                          |
| `$SendTo`             | Specifies the logging destination. Set to `"LogAnalytics"` or `"Datadog"`.                   |


## Usage

1. Clone this repository or download the script file.
2. Open the script file and update the required variables.
3. Open a PowerShell terminal and run the script using the following command:

   ```powershell
   .\Enable-DiagnosticSettings.ps1

## Example Usage

### Sending Logs to Log Analytics Workspace

Set the following variables in the script:

```powershell
$ResourceGroupName = "MyResourceGroup"
$WorkspaceResourceId = "/subscriptions/<subscription-id>/resourceGroups/<rg-name>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>"
$SendTo = "LogAnalytics"


### Sending Logs to Datadog

Set the following variables in the script:

```powershell
$ResourceGroupName = "MyResourceGroup"
$DatadogEndpoint = "https://<datadog-endpoint>"
$SendTo = "Datadog"

