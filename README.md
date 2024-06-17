# Repository Automation with Mergeable

This repository uses the Mergeable GitHub App to automate and streamline pull request (PR) management. The rules specified in the `mergeable.yml` file help manage PR interactions effectively.

## Configuration Details

### `mergeable.yml`

The `mergeable.yml` file contains rules that automate several key actions on pull requests:

1. **Greet a Contributor and Request Reviewers**
   - **Trigger**: When a pull request is opened.
   - **Actions**:
     - **Request Review**: Automatically requests reviews from specified senior reviewer teams based on the PR's content (Android, Apple, Windows platforms).
     - **Assign PR**: Assigns the PR to the author for tracking and responsibility.
     - **Comment**: Posts a welcoming comment thanking the contributor and informing them that the team will review the changes shortly.

2. **Ensure Compliance and Approvals**
   - **Trigger**: On any updates to PRs, including reviews, status changes, and checks.
   - **Validation**:
     - Requires at least two approvals from code owners, ensuring that changes are thoroughly vetted.
   - **Actions**:
     - Marks checks as successful only after meeting the required approvals, maintaining high code quality and adherence to project standards.

### Summary

These automations facilitate a more efficient PR review process, ensure consistent communication, and maintain high standards of code integrity and compliance.
 to open an issue or submit a pull request if you have suggestions or need assistance.

