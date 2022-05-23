resource "azurerm_resource_group" "example" {
  name     = "example-rg-4270"
  location = "West Europe"
}

resource "azurerm_log_analytics_workspace" "example" {
  name                = "exampleworkspace4270"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
  sku                 = "PerGB2018"
}

resource "azurerm_log_analytics_solution" "example" {
  solution_name         = "SecurityInsights"
  location              = azurerm_resource_group.example.location
  resource_group_name   = azurerm_resource_group.example.name
  workspace_resource_id = azurerm_log_analytics_workspace.example.id
  workspace_name        = azurerm_log_analytics_workspace.example.name
  plan {
    publisher = "Microsoft"
    product   = "OMSGallery/SecurityInsights"
  }
}

resource "azurerm_sentinel_data_connector_azure_active_directory" "example" {
  name                       = "exampleaad4270"
  log_analytics_workspace_id = azurerm_log_analytics_solution.example.workspace_resource_id
}
resource "azurerm_sentinel_data_connector_azure_advanced_threat_protection" "example" {
  name                       = "example-adv-threat-protection"
  log_analytics_workspace_id = azurerm_log_analytics_solution.example.workspace_resource_id
}
resource "azurerm_sentinel_data_connector_azure_security_center" "example" {
  name                       = "example-azure-security-center"
  log_analytics_workspace_id = azurerm_log_analytics_solution.example.workspace_resource_id
}
resource "azurerm_sentinel_data_connector_microsoft_cloud_app_security" "example" {
  name                       = "cloud_app_security"
  log_analytics_workspace_id = azurerm_log_analytics_solution.example.workspace_resource_id
}
resource "azurerm_sentinel_data_connector_microsoft_defender_advanced_threat_protection" "example" {
  name                       = "advanced_threat_protection"
  log_analytics_workspace_id = azurerm_log_analytics_solution.example.workspace_resource_id
}
resource "azurerm_sentinel_data_connector_office_365" "example" {
  name                       = "office_365"
  log_analytics_workspace_id = azurerm_log_analytics_solution.example.workspace_resource_id
}
resource "azurerm_sentinel_data_connector_threat_intelligence" "example" {
  name                       = "threat_intelligence"
  log_analytics_workspace_id = azurerm_log_analytics_solution.example.workspace_resource_id
}
