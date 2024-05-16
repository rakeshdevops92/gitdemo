# GitHub Repository Team Permission and File Management Script

This PowerShell script is designed to manage team permissions and create necessary configuration files across multiple repositories in a GitHub organization. Specifically, it ensures that the `hpx-devops` team has the required permissions on each repository and creates or updates specific files (`CODEOWNERS` and `mergeable.yml`) if they do not already exist.

## Prerequisites

- **GitHub Personal Access Token (PAT)**: The token should have the necessary permissions to manage team access and repository contents.
- **PowerShell**: Ensure PowerShell is installed on the system where the script will be executed.
- **Repository List File**: A text file containing a list of repository names (one per line) that you want to manage.

## Usage

### Parameters

- **token**: (Optional) GitHub Personal Access Token. If not provided, it should be securely handled in your Azure Pipelines.
- **repositorylist**: (Mandatory) Path to the text file containing the list of repositories.

### Script Execution

1. **Save the Script**: Save the PowerShell script to a file, e.g., `UpdateRepos.ps1`.
2. **Prepare the Repository List**: Create a text file (e.g., `repositorylist.txt`) with the names of the repositories you want to manage, one per line.
3. **Run the Script Locally**: You can test the script locally using the following command:
   ```powershell
   ./UpdateRepos.ps1 -token "YOUR_GITHUB_PAT" -repositorylist "path/to/repositorylist.txt"
