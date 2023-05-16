# Provider configuration
provider "azurerm" {
  features {}
}

# Create Azure Databricks workspace
resource "azurerm_databricks_workspace" "example" {
  name                = "example-databricks-workspace"
  resource_group_name = azurerm_resource_group.example.name
  location            = azurerm_resource_group.example.location
  sku                 = "standard"
}

# Create Databricks cluster with specific Spark version and libraries
resource "azurerm_databricks_cluster" "example" {
  name              = "example-cluster"
  resource_group_id = azurerm_resource_group.example.id
  workspace_id      = azurerm_databricks_workspace.example.id
  spark_version     = "7.3.x-scala2.12"
  
  spark_conf {
    "spark.databricks.libraries" = "dbfs:/libraries/example-library.jar,dbfs:/libraries/other-library.whl"
  }
}

# Create Databricks SQL workspace with specific warehouse type
resource "azurerm_databricks_sql_workspace" "example" {
  name              = "example-sql-workspace"
  resource_group_id = azurerm_resource_group.example.id
  workspace_id      = azurerm_databricks_workspace.example.id
  warehouse         = "Small"
}

# Create Databricks job with specified schedule, parameters, and job path
resource "azurerm_databricks_job" "example" {
  name              = "example-job"
  resource_group_id = azurerm_resource_group.example.id
  workspace_id      = azurerm_databricks_workspace.example.id
  
  schedule {
    quartz_cron_expression = "0 0 12 * * ?"  # Run daily at 12:00 PM
  }
  
  notebook_task {
    notebook_path = "/jobs/example-notebook"
  }
  
  # Additional parameters can be configured as required
  spark_python_task {
    python_file = "dbfs:/jobs/example-script.py"
  }
}

# Configure GitHub integration for Databricks pipeline configuration
resource "azurerm_databricks_instance_profile" "example" {
  name              = "example-instance-profile"
  resource_group_id = azurerm_resource_group.example.id
  workspace_id      = azurerm_databricks_workspace.example.id
  instance_profile_arn = "<instance-profile-arn>"
  role_arn = "<role-arn>"
}

resource "azurerm_databricks_secret_scope" "example" {
  name              = "example-secret-scope"
  resource_group_id = azurerm_resource_group.example.id
  workspace_id      = azurerm_databricks_workspace.example.id
  scope_backend_type = "SECRETS"
  scope_backend_azure_key_vault {
    secret_scope_name = azurerm_databricks_secret_scope.example.name
    key_vault_url     = "<key-vault-url>"
  }
}

# User access control can be managed through the Databricks workspace itself
# Use Databricks CLI or APIs to manage user access and roles
