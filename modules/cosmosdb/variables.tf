variable "prefix" {
  type        = string
  description = "The prefix used for all resources in this environment"
}

variable "location" {
  type        = string
  description = "The Azure location where all resources in this  deployment should be created"
}

# variable "prevent_destroy" {
#   type        = string
#   description = "Should cosmodb life cycle to prevent getting recreated every time terraform runs"
# }

variable "resource_group_name" {
  type = string
  description = "The Azure resource name where all resources in this deployment should be created"
  
}