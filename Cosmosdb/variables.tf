# Cosmos DB variables
variable "name" {
  description = "Name of the Cosmos DB account"
  type        = string
}

variable "location" {
  description = "Location/Region where the resources will be created"
  type        = string
}

variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
}

variable "offer_type" {
  description = "Offer type for Cosmos DB, e.g., Standard"
  type        = string
}

variable "kind" {
  description = "Kind of Cosmos DB account, e.g., GlobalDocumentDB"
  type        = string
}

variable "enable_automatic_failover" {
  description = "Enable automatic failover for Cosmos DB"
  type        = bool
}

variable "public_network_access_enabled" {
  description = "Specifies if public network access is enabled"
  type        = bool
}

variable "capability_name" {
  description = "Name of the capability to enable (e.g., EnableServerless)"
  type        = string
}

variable "consistency_level" {
  description = "Consistency level of Cosmos DB"
  type        = string
}

variable "max_staleness_prefix" {
  description = "The maximum allowed staleness prefix for Bounded Staleness consistency"
  type        = number
}

variable "max_interval_in_seconds" {
  description = "The maximum interval in seconds for Bounded Staleness consistency"
  type        = number
}

variable "failover_priority" {
  description = "Failover priority of the Cosmos DB geo-location"
  type        = number
}

variable "backup_type" {
  description = "Type of backup for Cosmos DB (e.g., Periodic)"
  type        = string
}

variable "backup_interval_in_minutes" {
  description = "Backup interval in minutes"
  type        = number
}

variable "backup_retention_in_hours" {
  description = "Backup retention in hours"
  type        = number
}

variable "backup_storage_redundancy" {
  description = "Storage redundancy for backups (e.g., Local)"
  type        = string
}

# Private Endpoint variables
variable "private_endpoint_name" {
  description = "Name of the private endpoint"
  type        = string
}

variable "subnet_id" {
  description = "ID of the subnet where the private endpoint will be created"
  type        = string
}

variable "private_service_connection_name" {
  description = "Name of the private service connection"
  type        = string
}

variable "subresource_names" {
  description = "Subresource names for the private service connection (e.g., Sql)"
  type        = list(string)
}

variable "is_manual_connection" {
  description = "Specifies if the connection is manual"
  type        = bool
}

variable "private_dns_zone_group_name" {
  description = "Name of the private DNS zone group"
  type        = string
}

variable "private_dns_zone_ids" {
  description = "List of private DNS zone IDs"
  type        = list(string)
}

# Diagnostic Setting variables
variable "diag_setting_name" {
  description = "Name of the diagnostic setting"
  type        = string
}

variable "log_analytics_workspace_id" {
  description = "ID of the Log Analytics Workspace"
  type        = string
}

variable "log_category_group" {
  description = "Category group for logs"
  type        = string
}

variable "metric_category" {
  description = "Category for metrics"
  type        = string
}

# Tags
variable "tags" {
  description = "Tags to apply to the resources"
  type        = map(string)
  default     = {}
}

# Lifecycle Ignore Changes
variable "ignore_changes" {
  description = "List of properties to ignore during Terraform apply"
  type        = list(string)
  default     = ["tags", "identity", "ip_range_filter", "virtual_network_rule", "is_virtual_network_filter_enabled", "public_network_access_enabled"]
}
