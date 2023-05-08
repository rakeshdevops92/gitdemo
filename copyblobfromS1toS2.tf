// Configure the AzureRM provider for Terraform.
provider "azurerm" {
  features {}
}

// Create a resource group where all resources will be deployed.
resource "azurerm_resource_group" "exasdf" {
  name     = "exasdf-resources"
  location = "West Europe"
}

// Create a storage account to be used as the source of the files to be synced.
resource "azurerm_storage_account" "source" {
  name                     = "exasdfstoragesource"
  resource_group_name      = azurerm_resource_group.exasdf.name
  location                 = azurerm_resource_group.exasdf.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

// Create a storage account to be used as the destination of the files to be synced.
resource "azurerm_storage_account" "destination" {
  name                     = "exasdfstoragedestination"
  resource_group_name      = azurerm_resource_group.exasdf.name
  location                 = azurerm_resource_group.exasdf.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

// Create a container in the source storage account where the files to be synced are located.
resource "azurerm_storage_container" "source_container" {
  name                  = "source-container"
  storage_account_name  = azurerm_storage_account.source.name
}

// Create a container in the destination storage account where the files will be synced to.
resource "azurerm_storage_container" "destination_container" {
  name                  = "destination-container"
  storage_account_name  = azurerm_storage_account.destination.name
}

// Create an App Service Plan to host the Azure Function App.
resource "azurerm_app_service_plan" "exasdf" {
  name                = "exasdf-appserviceplan"
  location            = azurerm_resource_group.exasdf.location
  resource_group_name = azurerm_resource_group.exasdf.name
  kind                = "FunctionApp"

  // Configure the SKU for the App Service Plan.
  sku {
    tier = "Dynamic"
    size = "Y1"
  }
}

// Create an Azure Function App to sync the files from the source storage account to the destination storage account.
resource "azurerm_function_app" "exasdf" {
  name                       = "exasdf-functionapp"
  location                   = azurerm_resource_group.exasdf.location
  resource_group_name        = azurerm_resource_group.exasdf.name
  app_service_plan_id        = azurerm_app_service_plan.exasdf.id
  storage_account_name       = azurerm_storage_account.source.name
  storage_account_access_key = azurerm_storage_account.source.primary_access_key
  version                    = "~4"

  // Configure the app settings for the Azure Function App.
  app_settings = {
    "AzureWebJobsStorage"           = "DefaultEndpointsProtocol=https;AccountName=${azurerm_storage_account.source.name};AccountKey=${azurerm_storage_account.source.primary_access_key};EndpointSuffix=core.windows.net"
    "FUNCTIONS_WORKER_RUNTIME"      = "dotnet"
    "WEBSITE_RUN_FROM_PACKAGE"      = "1"
    "SOURCE_STORAGE_ACCOUNT_NAME"   = azurerm_storage_account.source.name
    "SOURCE_STORAGE_ACCOUNT_KEY"    = azurerm_storage_account.source.primary_access_key
    "DESTINATION_STORAGE_ACCOUNT_NAME" = azurerm_storage_account.destination.name
    "DESTINATION_STORAGE_ACCOUNT_KEY"  = azurerm_storage_account.destination.primary_access_key
  }
}
