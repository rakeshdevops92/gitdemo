resource "azurerm_resource_group" "example" {
  name     = "api-rg-pro-4270"
  location = "West Europe"
}

resource "azurerm_app_service_plan" "example" {
  name                = "api-appserviceplan-pro-4270"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
  zone_redundant       = true
  kind = "elastic"

  sku {
    tier = "ElasticPremium"
    size = "EP1"
  }
}
