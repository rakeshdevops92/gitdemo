resource "azurerm_user_assigned_identity" "example" {
  resource_group_name = "DefaultResourceGroup-CUS"
  location            = "east us"

  name = "search-api"
}

data "azurerm_storage_account" "example" {
  name                = "testasdf"
  resource_group_name = "DefaultResourceGroup-CUS"
}

resource "azurerm_role_assignment" "example" {
  scope                = data.azurerm_storage_account.example.identity.0.principal_id
  role_definition_name = "Reader"
  principal_id         = azurerm_user_assigned_identity.example.principal_id
}

data "azurerm_subscription" "primary" {
}
