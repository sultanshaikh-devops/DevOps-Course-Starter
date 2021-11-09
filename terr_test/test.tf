terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 2.49"
    }
  }
  backend "azurerm" {
    resource_group_name  = "OpenCohort1_SultanShaikh_ProjectExercise"
    storage_account_name = "tfstate007ss"
    container_name       = "tfstate007ss"
    key                  = "terraform.tfstate"
  }
}
provider "azurerm" {
  features {}
}

module "cosmosdb" {
  source              = "./modules/cosmosdb"
  prefix              = var.prefix
  location            = var.location
  resource_group_name = var.resource_group_name  
}

data "azurerm_cosmosdb_account" "main" {
  name                = "${var.prefix}-cosmosdb-account"
  resource_group_name = var.resource_group_name
}
