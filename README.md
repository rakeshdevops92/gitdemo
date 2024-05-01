# Branch Protection Management Script

## Overview
This PowerShell script is designed to automate the management of GitHub branch protection rules. It retrieves branch protection settings from a specified source branch and applies these settings to multiple destination branches across different repositories.

## Features
- **Retrieve Protection Rules**: Fetches the branch protection rules from a source branch.
- **Apply Protection Rules**: Applies the fetched rules to specified destination branches in multiple repositories.
- **Customizable**: Easily adaptable for different repositories and branches.
- **Logging**: Provides detailed logging of operations for troubleshooting and verification.

## Prerequisites
- **PowerShell**: The script is written for PowerShell and requires PowerShell to be installed on the machine where it's executed.
- **GitHub Personal Access Token**: A personal access token with sufficient permissions to manage branch protections in the target repositories.

## Setup
1. **Secure File with Repositories**: Maintain a list of repository names in an Azure DevOps secure file.
2. **Personal Access Token**: Ensure your GitHub Personal Access Token (PAT) has the necessary permissions. This token must be able to read and write branch protection settings.

## Configuration
Update the script variables at the beginning of the script:
- `sourceOwner`: Owner of the source repository.
- `sourceRepo`: Source repository from which to copy the branch protection rules.
- `sourceBranch`: Branch in the source repository from which to copy the protection rules.
- `destinationOwner`: Owner of the destination repositories.
- `destinationBranch`: Branch name where the rules will be applied.

## Usage
1. **Configure your PAT and repository details** in the script.
2. **Run the script** in PowerShell:
   ```bash
   .\manage-branch-protection.ps1
