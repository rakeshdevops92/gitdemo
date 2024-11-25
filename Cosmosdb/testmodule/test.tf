module "cosmosdb" {
  source = "./modules/cosmosdb"

  name                          = "my-cosmosdb-account"
  location                      = "eastus"
  resource_group_name           = "my-resource-group"
  offer_type                    = "Standard"
  kind                          = "GlobalDocumentDB"
  enable_automatic_failover     = true
  public_network_access_enabled = false
  capability_name               = "EnableServerless"
  consistency_level             = "BoundedStaleness"
  max_staleness_prefix          = 100
  max_interval_in_seconds       = 5
  failover_priority             = 0
  backup_type                   = "Periodic"
  backup_interval_in_minutes    = 240
  backup_retention_in_hours     = 168
  backup_storage_redundancy     = "Local"

  private_endpoint_name          = "my-private-endpoint"
  subnet_id                      = "/subscriptions/.../subnets/my-subnet"
  private_service_connection_name = "my-service-connection"
  subresource_names              = ["Sql"]
  is_manual_connection           = false
  private_dns_zone_group_name    = "default"
  private_dns_zone_ids           = ["/subscriptions/.../dnszones/my-private-dns-zone"]

  diag_setting_name             = "my-diagnostics"
  log_analytics_workspace_id    = "/subscriptions/.../resourceGroups/.../providers/Microsoft.OperationalInsights/workspaces/my-law"
  log_category_group            = "alllogs"
  metric_category               = "AllMetrics"

  tags = {
    environment = "dev"
  }
}
