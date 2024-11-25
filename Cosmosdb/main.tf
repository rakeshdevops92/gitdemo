resource "azurerm_cosmosdb_account" "example" {
  lifecycle {
    ignore_changes = var.ignore_changes
  }
  name                          = var.name
  location                      = var.location
  resource_group_name           = var.resource_group_name
  offer_type                    = var.offer_type
  kind                          = var.kind
  enable_automatic_failover     = var.enable_automatic_failover
  public_network_access_enabled = var.public_network_access_enabled

  capabilities {
    name = var.capability_name
  }

  consistency_policy {
    consistency_level       = var.consistency_level
    max_staleness_prefix    = var.max_staleness_prefix
    max_interval_in_seconds = var.max_interval_in_seconds
  }

  geo_location {
    location          = var.location
    failover_priority = var.failover_priority
  }

  backup {
    type                = var.backup_type
    interval_in_minutes = var.backup_interval_in_minutes
    retention_in_hours  = var.backup_retention_in_hours
    storage_redundancy  = var.backup_storage_redundancy
  }
}

resource "azurerm_private_endpoint" "peocs1" {
  name                = var.private_endpoint_name
  location            = var.location
  resource_group_name = var.resource_group_name
  subnet_id           = var.subnet_id

  private_service_connection {
    name                           = var.private_service_connection_name
    private_connection_resource_id = azurerm_cosmosdb_account.example.id
    subresource_names              = var.subresource_names
    is_manual_connection           = var.is_manual_connection
  }

  private_dns_zone_group {
    name                 = var.private_dns_zone_group_name
    private_dns_zone_ids = var.private_dns_zone_ids
  }

  tags = var.tags
}

resource "azurerm_monitor_diagnostic_setting" "example" {
  name                       = var.diag_setting_name
  target_resource_id         = azurerm_cosmosdb_account.example.id
  log_analytics_workspace_id = var.log_analytics_workspace_id

  enabled_log {
    category_group = var.log_category_group
  }

  metric {
    category = var.metric_category
  }
}
