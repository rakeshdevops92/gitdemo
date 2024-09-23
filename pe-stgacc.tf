resource "azurerm_private_endpoint" "example" {
  name                = var.private_endpoint_name
  location            = var.location
  resource_group_name = var.resource_group_name
  subnet_id           = var.subnet_id

  private_service_connection {
    name                           = "examplePrivateServiceConnection"
    is_manual_connection           = false
    private_connection_resource_id = var.storage_account_id
    subresource_names              = ["blob", "file"]
  }

  tags = var.tags
}





variable "private_endpoint_name" {
  description = "Name of the private endpoint"
  type        = string
}

variable "location" {
  description = "Location of the resources"
  type        = string
}

variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
}

variable "subnet_id" {
  description = "ID of the subnet where the private endpoint will be created"
  type        = string
}

variable "storage_account_id" {
  description = "ID of the storage account to associate with the private endpoint"
  type        = string
}

variable "tags" {
  description = "A map of tags to assign to the resource"
  type        = map(string)
  default     = {}
}





module "private_endpoint" {
  source = "./modules/private_endpoint"

  private_endpoint_name = var.private_endpoint_name
  location              = var.location
  resource_group_name   = var.resource_group_name
  subnet_id             = var.subnet_id
  storage_account_id    = var.storage_account_id
  tags                  = var.tags
}



variable "private_endpoint_name" {
  description = "Name of the private endpoint"
  type        = string
}

variable "location" {
  description = "Location of the resources"
  type        = string
}

variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
}

variable "subnet_id" {
  description = "ID of the subnet where the private endpoint will be created"
  type        = string
}

variable "storage_account_id" {
  description = "ID of the storage account to associate with the private endpoint"
  type        = string
}

variable "tags" {
  description = "A map of tags to assign to the resource"
  type        = map(string)
  default     = {}
}
